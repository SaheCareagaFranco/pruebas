import streamlit as st
import sqlite3
import os

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Kuna Capital | Bonos",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Kuna Capital Design System
# Colors: Navy #002236, Green #1AC77C, Black #171D1C, Neutral-50 #F6F7F7
# Fonts: Outfit (headlines) + Noto Sans (body)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Noto+Sans:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
  font-family: 'Noto Sans', sans-serif;
  background-color: #F6F7F7;
  color: #171D1C;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
  padding: 0 !important;
  max-width: 100% !important;
}
section[data-testid="stSidebar"] { display: none; }

/* ========== NAVBAR ========== */
.kc-nav {
  background: #002236;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 48px;
  border-bottom: 3px solid #1AC77C;
  margin-bottom: 0;
}
.kc-nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}
.kc-nav-brand .dot {
  width: 10px; height: 10px;
  background: #1AC77C;
  border-radius: 50%;
  display: inline-block;
}
.kc-nav-brand .name {
  font-family: 'Outfit', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #FFFFFF;
  letter-spacing: 0.3px;
}
.kc-nav-brand .name span { color: #1AC77C; }
.kc-nav-brand .module {
  font-family: 'Noto Sans', sans-serif;
  font-size: 11px;
  color: #748C86;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-left: 6px;
  padding-left: 10px;
  border-left: 1px solid #323D3A;
}
.kc-nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.kc-chip {
  background: rgba(26,199,124,0.12);
  border: 1px solid rgba(26,199,124,0.3);
  color: #1AC77C;
  padding: 5px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-family: 'Noto Sans', sans-serif;
  font-weight: 500;
}
.kc-badge-admin {
  background: #1AC77C;
  color: #002236;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 700;
  font-family: 'Outfit', sans-serif;
  letter-spacing: 1.5px;
  text-transform: uppercase;
}
.kc-badge-user {
  background: rgba(255,255,255,0.1);
  color: #C0CEC9;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  font-family: 'Outfit', sans-serif;
  letter-spacing: 1px;
  text-transform: uppercase;
}

/* ========== LAYOUT WRAPPER ========== */
.kc-body {
  max-width: 1200px;
  margin: 0 auto;
  padding: 36px 32px;
}

/* ========== WELCOME BANNER ========== */
.kc-hero {
  background: linear-gradient(135deg, #002236 0%, #00304C 100%);
  border-radius: 16px;
  padding: 32px 36px;
  margin-bottom: 28px;
  position: relative;
  overflow: hidden;
}
.kc-hero::before {
  content: '';
  position: absolute;
  top: -40px; right: -40px;
  width: 200px; height: 200px;
  background: rgba(26,199,124,0.06);
  border-radius: 50%;
}
.kc-hero::after {
  content: '';
  position: absolute;
  bottom: -60px; right: 80px;
  width: 280px; height: 280px;
  background: rgba(26,199,124,0.04);
  border-radius: 50%;
}
.kc-hero h1 {
  font-family: 'Outfit', sans-serif;
  font-size: 26px;
  font-weight: 700;
  color: #FFFFFF;
  margin-bottom: 6px;
}
.kc-hero h1 span { color: #1AC77C; }
.kc-hero p {
  color: #748C86;
  font-size: 14px;
  font-weight: 400;
}
.kc-hero .tag {
  display: inline-block;
  background: rgba(26,199,124,0.15);
  border: 1px solid rgba(26,199,124,0.3);
  color: #1AC77C;
  font-size: 11px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 8px;
  margin-bottom: 14px;
  font-family: 'Outfit', sans-serif;
  letter-spacing: 1px;
  text-transform: uppercase;
}

/* ========== STAT CARDS ========== */
.kc-stat {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 22px 24px;
  box-shadow: 0 1px 8px rgba(0,0,0,0.06);
  border-top: 3px solid #1AC77C;
}
.kc-stat .s-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  color: #748C86;
  font-weight: 600;
  margin-bottom: 10px;
  font-family: 'Outfit', sans-serif;
}
.kc-stat .s-val {
  font-family: 'Outfit', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: #002236;
  line-height: 1;
}
.kc-stat .s-sub {
  font-size: 12px;
  color: #748C86;
  margin-top: 5px;
}

/* ========== SECTION TITLE ========== */
.kc-stitle {
  font-family: 'Outfit', sans-serif;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: #485856;
  padding-bottom: 10px;
  border-bottom: 2px solid #E0E7E4;
  margin-bottom: 16px;
}
.kc-stitle span { color: #1AC77C; }

/* ========== TABLE ========== */
.kc-tbl {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Noto Sans', sans-serif;
  font-size: 13px;
  background: #FFFFFF;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 8px rgba(0,0,0,0.06);
}
.kc-tbl thead tr {
  background: #002236;
}
.kc-tbl th {
  padding: 12px 16px;
  text-align: left;
  font-size: 11px;
  font-family: 'Outfit', sans-serif;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #1AC77C;
}
.kc-tbl td {
  padding: 13px 16px;
  border-bottom: 1px solid #E0E7E4;
  color: #2C3533;
}
.kc-tbl tr:last-child td { border-bottom: none; }
.kc-tbl tbody tr:hover td { background: #F6F7F7; }
.kc-green { font-weight: 700; color: #148152; }
.kc-pw {
  font-family: monospace;
  background: rgba(26,199,124,0.1);
  border: 1px solid rgba(26,199,124,0.2);
  color: #002236;
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

/* ========== ALERTS ========== */
.kc-ok {
  background: rgba(26,199,124,0.1);
  border-left: 4px solid #1AC77C;
  color: #148152;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 14px;
  margin-bottom: 16px;
}
.kc-err {
  background: rgba(220,50,50,0.08);
  border-left: 4px solid #DC3232;
  color: #991F1F;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 14px;
  margin-bottom: 16px;
}
.kc-empty {
  text-align: center;
  padding: 48px 20px;
  color: #C0CEC9;
  font-family: 'Noto Sans', sans-serif;
  background: #FFFFFF;
  border-radius: 12px;
}
.kc-empty .ico { font-size: 40px; display: block; margin-bottom: 10px; }

/* ========== LOGIN ========== */
.kc-login-bg {
  min-height: 92vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F6F7F7;
  padding: 40px 16px;
}
.kc-login-card {
  background: #FFFFFF;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0,34,54,0.12);
  padding: 52px 44px;
  width: 100%;
  max-width: 420px;
  border-top: 4px solid #1AC77C;
}
.kc-login-brand {
  text-align: center;
  margin-bottom: 36px;
}
.kc-login-brand .name {
  font-family: 'Outfit', sans-serif;
  font-size: 28px;
  font-weight: 800;
  color: #002236;
  letter-spacing: 0.3px;
}
.kc-login-brand .name span { color: #1AC77C; }
.kc-login-brand .sub {
  font-size: 11px;
  font-family: 'Noto Sans', sans-serif;
  color: #748C86;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  margin-top: 6px;
}
.kc-divider {
  width: 40px;
  height: 3px;
  background: #1AC77C;
  border-radius: 2px;
  margin: 12px auto 0;
}

/* ========== Streamlit overrides ========== */
.stButton > button {
  background: #002236 !important;
  color: #1AC77C !important;
  border: 1.5px solid #1AC77C !important;
  border-radius: 8px !important;
  font-family: 'Outfit', sans-serif !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  letter-spacing: 0.5px !important;
  transition: all 0.2s !important;
}
.stButton > button:hover {
  background: #1AC77C !important;
  color: #002236 !important;
}
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stDateInput"] input {
  border: 2px solid #E0E7E4 !important;
  border-radius: 8px !important;
  font-family: 'Noto Sans', sans-serif !important;
  color: #171D1C !important;
}
div[data-testid="stTextInput"] input:focus {
  border-color: #1AC77C !important;
  box-shadow: 0 0 0 2px rgba(26,199,124,0.15) !important;
}
div[data-testid="stSelectbox"] > div {
  border: 2px solid #E0E7E4 !important;
  border-radius: 8px !important;
}
label[data-testid="stWidgetLabel"] p,
.stTextInput label, .stSelectbox label,
.stNumberInput label, .stDateInput label {
  font-family: 'Outfit', sans-serif !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.8px !important;
  color: #485856 !important;
}
/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  background: transparent;
  gap: 4px;
  border-bottom: 2px solid #E0E7E4;
}
.stTabs [data-baseweb="tab"] {
  background: transparent;
  color: #748C86;
  font-family: 'Outfit', sans-serif;
  font-weight: 600;
  font-size: 13px;
  padding: 10px 24px;
  border-radius: 8px 8px 0 0;
  letter-spacing: 0.3px;
}
.stTabs [aria-selected="true"] {
  background: #002236 !important;
  color: #1AC77C !important;
}
/* Expander */
div[data-testid="stExpander"] {
  background: #FFFFFF;
  border: 1px solid #E0E7E4 !important;
  border-radius: 10px !important;
  margin-bottom: 16px;
}
summary {
  font-family: 'Outfit', sans-serif !important;
  font-weight: 600 !important;
  color: #002236 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Base de datos
# ---------------------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bonos.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT    UNIQUE NOT NULL,
            password TEXT    NOT NULL,
            nombre   TEXT    NOT NULL,
            rol      TEXT    NOT NULL DEFAULT 'usuario'
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS bonos (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            concepto   TEXT    NOT NULL,
            monto      REAL    NOT NULL,
            periodo    TEXT    NOT NULL,
            fecha      TEXT    NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)
    c.execute("SELECT id FROM usuarios WHERE username = 'admin'")
    if not c.fetchone():
        c.execute(
            "INSERT INTO usuarios (username, password, nombre, rol) VALUES (?, ?, ?, ?)",
            ("admin", "admin123", "Administrador", "admin"),
        )
    conn.commit()
    conn.close()


init_db()

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
defaults = dict(logged_in=False, user_id=None, username="", nombre="", rol="", admin_msg=None, login_error="")
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def logout():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()


# ---------------------------------------------------------------------------
# Navbar
# ---------------------------------------------------------------------------
def navbar():
    right = ""
    if st.session_state.logged_in:
        badge = "kc-badge-admin" if st.session_state.rol == "admin" else "kc-badge-user"
        label = "ADMIN" if st.session_state.rol == "admin" else "USUARIO"
        right = f'<span class="kc-chip">👤 {st.session_state.nombre}</span><span class="{badge}">{label}</span>'

    st.markdown(f"""
    <div class="kc-nav">
      <div class="kc-nav-brand">
        <span class="dot"></span>
        <div>
          <div class="name">KUNA <span>CAPITAL</span>
            <span class="module">Portal de Bonos</span>
          </div>
        </div>
      </div>
      <div class="kc-nav-right">{right}</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# LOGIN
# ---------------------------------------------------------------------------
def view_login():
    navbar()
    st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("""
        <div class="kc-login-card">
          <div class="kc-login-brand">
            <div class="name">KUNA <span>CAPITAL</span></div>
            <div class="sub">Portal de Bonos</div>
            <div class="kc-divider"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.login_error:
            st.markdown(f'<div class="kc-err">⚠ {st.session_state.login_error}</div>', unsafe_allow_html=True)
            st.session_state.login_error = ""

        with st.form("login", clear_on_submit=False):
            username = st.text_input("Usuario", placeholder="Tu usuario de acceso")
            password = st.text_input("Contraseña", type="password", placeholder="••••••••")
            st.markdown("<br>", unsafe_allow_html=True)
            ok = st.form_submit_button("Ingresar al portal", use_container_width=True)

        if ok:
            conn = get_db()
            user = conn.execute(
                "SELECT * FROM usuarios WHERE username=? AND password=?",
                (username.strip(), password.strip()),
            ).fetchone()
            conn.close()
            if user:
                st.session_state.logged_in = True
                st.session_state.user_id   = user["id"]
                st.session_state.username  = user["username"]
                st.session_state.nombre    = user["nombre"]
                st.session_state.rol       = user["rol"]
                st.rerun()
            else:
                st.session_state.login_error = "Usuario o contraseña incorrectos."
                st.rerun()

        st.markdown("""
        <p style="text-align:center;color:#C0CEC9;font-size:12px;margin-top:18px;
                  font-family:'Noto Sans',sans-serif;">
          Acceso restringido — solo personal autorizado
        </p>""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# USUARIO
# ---------------------------------------------------------------------------
def view_usuario():
    navbar()
    st.markdown("<div style='max-width:1100px;margin:0 auto;padding:32px 32px'>", unsafe_allow_html=True)

    conn  = get_db()
    bonos = conn.execute(
        "SELECT * FROM bonos WHERE usuario_id=? ORDER BY fecha DESC",
        (st.session_state.user_id,),
    ).fetchall()
    conn.close()

    total   = len(bonos)
    monto_t = sum(b["monto"] for b in bonos)
    ult_m   = bonos[0]["monto"] if bonos else 0
    ult_p   = bonos[0]["periodo"] if bonos else "—"

    st.markdown(f"""
    <div class="kc-hero">
      <div class="tag">Mi portal</div>
      <h1>Hola, <span>{st.session_state.nombre}</span> 👋</h1>
      <p>Consulta tus bonos registrados en Kuna Capital.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([1, 1, 1, 0.6])
    with c1:
        st.markdown(f'<div class="kc-stat"><div class="s-label">Bonos totales</div><div class="s-val">{total}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kc-stat"><div class="s-label">Monto acumulado</div><div class="s-val">${monto_t:,.2f}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kc-stat"><div class="s-label">Ultimo bono</div><div class="s-val">${ult_m:,.2f}</div><div class="s-sub">{ult_p}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Cerrar sesion", use_container_width=True):
            logout()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="kc-stitle">MIS <span>BONOS</span></div>', unsafe_allow_html=True)

    if bonos:
        rows = "".join(f"""<tr>
          <td>{i+1}</td>
          <td>{b['concepto']}</td>
          <td>{b['periodo']}</td>
          <td>{b['fecha']}</td>
          <td class="kc-green">${b['monto']:,.2f}</td>
        </tr>""" for i, b in enumerate(bonos))
        st.markdown(f"""
        <table class="kc-tbl">
          <thead><tr><th>#</th><th>Concepto</th><th>Periodo</th><th>Fecha</th><th>Monto</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="kc-empty"><span class="ico">📋</span><p>No tienes bonos registrados aun.<br>Contacta a tu administrador.</p></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# ADMIN
# ---------------------------------------------------------------------------
def view_admin():
    navbar()
    st.markdown("<div style='max-width:1200px;margin:0 auto;padding:32px 32px'>", unsafe_allow_html=True)

    conn     = get_db()
    usuarios = conn.execute("SELECT * FROM usuarios WHERE rol='usuario' ORDER BY nombre").fetchall()
    bonos    = conn.execute("""
        SELECT b.*, u.nombre as nu, u.username as un
        FROM bonos b JOIN usuarios u ON b.usuario_id=u.id
        ORDER BY b.fecha DESC
    """).fetchall()
    conn.close()

    # Hero + logout
    col_h, col_btn = st.columns([5, 1])
    with col_h:
        st.markdown("""
        <div class="kc-hero">
          <div class="tag">Administrador</div>
          <h1>Panel de <span>Administracion</span></h1>
          <p>Gestiona usuarios, bonos y contrasenas del portal.</p>
        </div>""", unsafe_allow_html=True)
    with col_btn:
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        if st.button("Cerrar sesion", use_container_width=True):
            logout()

    # Mensajes
    if st.session_state.admin_msg:
        msg, t = st.session_state.admin_msg
        cls = "kc-ok" if t == "s" else "kc-err"
        ico = "✓" if t == "s" else "✗"
        st.markdown(f'<div class="{cls}">{ico} {msg}</div>', unsafe_allow_html=True)
        st.session_state.admin_msg = None

    tab_u, tab_b = st.tabs(["👥   Usuarios", "💰   Bonos"])

    # ── TAB USUARIOS ──────────────────────────────────────────────────────────
    with tab_u:
        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("➕  Agregar nuevo usuario", expanded=True):
            with st.form("add_user", clear_on_submit=True):
                a, b, c = st.columns(3)
                with a: nombre   = st.text_input("Nombre completo", placeholder="Ej: Ana Lopez")
                with b: username = st.text_input("Username", placeholder="Ej: alopez")
                with c: password = st.text_input("Contraseña inicial", placeholder="••••••••")
                if st.form_submit_button("Agregar usuario"):
                    if not all([nombre.strip(), username.strip(), password.strip()]):
                        st.session_state.admin_msg = ("Todos los campos son obligatorios.", "e")
                    else:
                        try:
                            conn = get_db()
                            conn.execute(
                                "INSERT INTO usuarios (username,password,nombre,rol) VALUES(?,?,?,'usuario')",
                                (username.strip(), password.strip(), nombre.strip()),
                            )
                            conn.commit(); conn.close()
                            st.session_state.admin_msg = (f"Usuario '{nombre.strip()}' creado.", "s")
                        except sqlite3.IntegrityError:
                            st.session_state.admin_msg = (f"El username '{username.strip()}' ya existe.", "e")
                    st.rerun()

        st.markdown('<div class="kc-stitle">USUARIOS REGISTRADOS — <span>CONTRASEÑAS VISIBLES</span></div>', unsafe_allow_html=True)

        if usuarios:
            rows = "".join(f"""<tr>
              <td>{u['id']}</td>
              <td><strong>{u['nombre']}</strong></td>
              <td>{u['username']}</td>
              <td><span class="kc-pw">{u['password']}</span></td>
            </tr>""" for u in usuarios)
            st.markdown(f"""
            <table class="kc-tbl">
              <thead><tr><th>ID</th><th>Nombre</th><th>Username</th><th>Contraseña</th></tr></thead>
              <tbody>{rows}</tbody>
            </table>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("✏️  Editar o eliminar usuario"):
                opts = {f"{u['nombre']} ({u['username']})": u for u in usuarios}
                sel  = st.selectbox("Seleccionar usuario", list(opts.keys()), key="sel_edit_u")
                u    = opts[sel]
                col_e, col_d = st.columns([2, 1])
                with col_e:
                    with st.form("edit_user"):
                        n = st.text_input("Nombre", value=u["nombre"])
                        p = st.text_input("Contraseña", value=u["password"])
                        if st.form_submit_button("Guardar cambios"):
                            conn = get_db()
                            conn.execute("UPDATE usuarios SET nombre=?,password=? WHERE id=?", (n, p, u["id"]))
                            conn.commit(); conn.close()
                            st.session_state.admin_msg = ("Usuario actualizado.", "s")
                            st.rerun()
                with col_d:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button(f"Eliminar a {u['nombre']}", type="primary"):
                        conn = get_db()
                        conn.execute("DELETE FROM bonos WHERE usuario_id=?", (u["id"],))
                        conn.execute("DELETE FROM usuarios WHERE id=?", (u["id"],))
                        conn.commit(); conn.close()
                        st.session_state.admin_msg = (f"'{u['nombre']}' eliminado.", "s")
                        st.rerun()
        else:
            st.markdown('<div class="kc-empty"><span class="ico">👥</span><p>No hay usuarios registrados.</p></div>', unsafe_allow_html=True)

    # ── TAB BONOS ─────────────────────────────────────────────────────────────
    with tab_b:
        st.markdown("<br>", unsafe_allow_html=True)

        if usuarios:
            with st.expander("➕  Asignar bono a un usuario", expanded=True):
                with st.form("add_bono", clear_on_submit=True):
                    r1c1, r1c2 = st.columns(2)
                    with r1c1:
                        umap = {f"{u['nombre']} ({u['username']})": u["id"] for u in usuarios}
                        sel_u = st.selectbox("Usuario", list(umap.keys()))
                        concepto = st.text_input("Concepto", placeholder="Ej: Bono de desempeno Q1 2025")
                    with r1c2:
                        monto   = st.number_input("Monto ($)", min_value=0.0, step=500.0, format="%.2f")
                        periodo = st.text_input("Periodo", placeholder="Ej: Q1 2025, Enero 2025")
                        fecha   = st.date_input("Fecha")
                    if st.form_submit_button("Asignar bono"):
                        if not concepto.strip() or not periodo.strip():
                            st.session_state.admin_msg = ("Concepto y periodo son obligatorios.", "e")
                        else:
                            conn = get_db()
                            conn.execute(
                                "INSERT INTO bonos (usuario_id,concepto,monto,periodo,fecha) VALUES(?,?,?,?,?)",
                                (umap[sel_u], concepto.strip(), monto, periodo.strip(), str(fecha)),
                            )
                            conn.commit(); conn.close()
                            st.session_state.admin_msg = ("Bono asignado exitosamente.", "s")
                        st.rerun()
        else:
            st.info("Primero agrega usuarios para poder asignarles bonos.")

        st.markdown('<div class="kc-stitle">TODOS LOS <span>BONOS</span></div>', unsafe_allow_html=True)

        if bonos:
            rows = "".join(f"""<tr>
              <td>{b['id']}</td>
              <td>{b['nu']}</td>
              <td>{b['concepto']}</td>
              <td>{b['periodo']}</td>
              <td>{b['fecha']}</td>
              <td class="kc-green">${b['monto']:,.2f}</td>
            </tr>""" for b in bonos)
            st.markdown(f"""
            <table class="kc-tbl">
              <thead><tr><th>ID</th><th>Usuario</th><th>Concepto</th><th>Periodo</th><th>Fecha</th><th>Monto</th></tr></thead>
              <tbody>{rows}</tbody>
            </table>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("🗑️  Eliminar bono"):
                bopts = {f"#{b['id']} — {b['nu']} | {b['concepto']} | ${b['monto']:,.2f}": b["id"] for b in bonos}
                sel_b = st.selectbox("Seleccionar bono", list(bopts.keys()), key="sel_del_b")
                if st.button("Eliminar bono seleccionado", type="primary"):
                    conn = get_db()
                    conn.execute("DELETE FROM bonos WHERE id=?", (bopts[sel_b],))
                    conn.commit(); conn.close()
                    st.session_state.admin_msg = ("Bono eliminado.", "s")
                    st.rerun()
        else:
            st.markdown('<div class="kc-empty"><span class="ico">💰</span><p>No hay bonos registrados aun.</p></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
if not st.session_state.logged_in:
    view_login()
elif st.session_state.rol == "admin":
    view_admin()
else:
    view_usuario()
