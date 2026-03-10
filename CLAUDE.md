# CLAUDE.md — Kuna Capital Bonos Intranet

This file provides guidance for AI assistants working on this codebase.

---

## Project Overview

**Kuna Capital Bonos Intranet** is an internal web application for managing employee bonuses. It has two implementations that coexist:

| File | Framework | Status |
|------|-----------|--------|
| `streamlit_app.py` | Streamlit | **Primary / active** |
| `app.py` | Flask | Legacy — kept for reference |
| `templates/` | Jinja2 HTML | Belongs to the Flask app |

All new development should target `streamlit_app.py`.

---

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Start the Streamlit app (primary)
streamlit run streamlit_app.py

# Start the Flask app (legacy, not in active use)
python app.py
```

- Streamlit listens on **port 8501** by default.
- Flask listens on **port 5000**.
- The SQLite database file `bonos.db` is created automatically on first run.

**Default admin credentials:**
- Username: `admin`
- Password: `admin123`

---

## Architecture

### Database (SQLite — `bonos.db`)

Five tables, all created by `init_db()` at startup:

| Table | Purpose |
|-------|---------|
| `usuarios` | Users with roles (`admin` / `usuario`) |
| `bonos` | Bonus records linked to a user |
| `listas` | Named groups of users |
| `lista_usuarios` | Many-to-many: list ↔ user |
| `bonos_vistos` | Tracks which bonuses a user has seen (for notifications) |

Schema is hardcoded in `init_db()`. There is no migrations framework — if you need a schema change, update `init_db()` and drop/recreate the database locally.

### Authentication & Sessions

- Streamlit uses `st.session_state` for auth state.
- Flask uses server-side sessions with a hardcoded secret key.
- Roles: `admin` (full CRUD) and `usuario` (read-only, own bonuses only).

### Routing (Streamlit)

Navigation is driven by `st.session_state["view"]`. The main views are:

| `view` value | Function | Access |
|---|---|---|
| `"login"` | `view_login()` | Public |
| `"admin_bonos"` | `view_admin_bonos()` | Admin |
| `"admin_usuarios"` | `view_admin_usuarios()` | Admin |
| `"user_bonos"` | `view_user_bonos()` | User |

The sidebar is rendered by `render_sidebar()` and is hidden on the login view.

---

## Key Conventions

### Database Access

Always use the `get_db()` helper — never call `sqlite3.connect()` directly:

```python
conn = get_db()
cur = conn.cursor()
cur.execute("SELECT ...", (param,))
conn.commit()   # after writes
conn.close()
```

Use parameterized queries (`?` placeholders) for all user-supplied values. Never interpolate strings into SQL.

### Session State

Read and write auth state through `st.session_state`:

```python
st.session_state["logged_in"]   # bool
st.session_state["user_id"]     # int
st.session_state["username"]    # str
st.session_state["nombre"]      # str (display name)
st.session_state["rol"]         # "admin" | "usuario"
st.session_state["view"]        # current view name
```

To navigate programmatically:

```python
st.session_state["view"] = "admin_bonos"
st.rerun()
```

### CSV Export

Use the `build_csv(rows, campos)` helper. It outputs UTF-8 with BOM so that Excel opens it correctly without encoding issues.

```python
csv_data = build_csv(rows, ["Concepto", "Monto", "Periodo", "Fecha"])
st.download_button("Exportar CSV", csv_data, "bonos.csv", "text/csv")
```

### Avatar / Initials

```python
initials(nombre)  # Returns up to 2 uppercase initials from a full name
```

### Logout

```python
logout()   # Clears all session state keys and triggers rerun
```

---

## Branding & Styling

All UI must follow Kuna Capital brand guidelines:

| Token | Value | Usage |
|-------|-------|-------|
| `#1AC77C` | Kuna Green | Primary actions, active states, accents |
| `#0A1628` | Navy | Sidebar background, headings |
| `#F6F7F7` | Light Gray | Page background |
| `#FFFFFF` | White | Card backgrounds |
| `#171D1C` | Near-black | Body text |

**Typography:** Google Fonts — `Outfit` (primary) and `Noto Sans` (secondary). Both are loaded via `<link>` tags inside `st.markdown()` HTML blocks.

Custom CSS is injected with `st.markdown("<style>...</style>", unsafe_allow_html=True)` at the top of each view function. Keep new styles consistent with existing patterns; avoid inline `style=` attributes on individual elements.

The Streamlit theme is declared in `.streamlit/config.toml` and must not be changed without design approval.

---

## Security Notes

The following known issues exist in the codebase. Do **not** regress them further; fixing them is welcome:

1. **Passwords are stored in plain text.** Migrate to `bcrypt` or `hashlib.pbkdf2_hmac` before any production deployment.
2. **Hardcoded Flask secret key** in `app.py` (`intranet_bonos_secret_key_2024`). Move to an environment variable.
3. **XSRF protection is disabled** in `.streamlit/config.toml`. Re-enable before going public.
4. **Debug mode enabled** in `app.py` (`app.run(debug=True)`). Disable in production.

---

## What Not to Touch

- `app.py` and `templates/` — legacy Flask code; do not add new features there.
- `.streamlit/config.toml` theme values — brand-approved, do not change colors.
- The `bonos_vistos` table logic — the notification badge depends on it.

---

## No Test Suite

There is currently no automated test framework. When making changes:

- Manually verify login, logout, and role-based access.
- Verify CSV export opens correctly in Excel (check UTF-8 BOM handling).
- Check that new bonuses trigger the notification badge for the target user.
- Confirm the database initializes cleanly on a fresh `bonos.db`.

---

## Adding Features

1. Add new view functions following the naming convention `view_<name>()`.
2. Register the view in `render_sidebar()` and add a routing case in the main block.
3. Guard admin-only views by checking `st.session_state["rol"] == "admin"` at the top of the function and redirecting to `"user_bonos"` if unauthorized.
4. Keep all database schema changes inside `init_db()`; document any column additions here.
