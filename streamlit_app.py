import streamlit as st
import sqlite3
import os
import pandas as pd

# ---------------------------------------------------------------------------
# Configuracion de pagina
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Kuna Capital | Bonos",
    page_icon="assets/logo.png" if os.path.exists("assets/logo.png") else "💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Estilos Kuna Capital
# ---------------------------------------------------------------------------
st.markdown("""
<style>
  /* ---- Fuentes y reset ---- */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  /* ---- Fondo general ---- */
  .stApp {
    background-color: #F7F8FC;
  }

  /* ---- Ocultar elementos de Streamlit ---- */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 0 !important; }

  /* ---- Navbar superior ---- */
  .kc-navbar {
    background: linear-gradient(135deg, #0A1628 0%, #122040 60%, #1A2F58 100%);
    padding: 0 40px;
    height: 68px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: -1rem -1rem 0 -1rem;
    box-shadow: 0 3px 20px rgba(0,0,0,0.35);
    border-bottom: 2px solid #C9A84C;
  }
  .kc-navbar-brand {
    display: flex;
    align-items: center;
    gap: 14px;
  }
  .kc-logo-text {
    font-size: 22px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: 0.5px;
  }
  .kc-logo-text span {
    color: #C9A84C;
  }
  .kc-tagline {
    font-size: 11px;
    color: rgba(255,255,255,0.5);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: -2px;
  }
  .kc-navbar-right {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .kc-user-chip {
    background: rgba(201,168,76,0.15);
    border: 1px solid rgba(201,168,76,0.4);
    color: #C9A84C;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
  }
  .kc-role-badge {
    background: #C9A84C;
    color: #0A1628;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
  }

  /* ---- Login card ---- */
  .kc-login-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 85vh;
    padding: 40px 16px;
  }
  .kc-login-card {
    background: #FFFFFF;
    border-radius: 16px;
    box-shadow: 0 20px 60px rgba(10,22,40,0.15);
    padding: 52px 44px;
    width: 100%;
    max-width: 420px;
    border-top: 4px solid #C9A84C;
  }
  .kc-login-logo {
    text-align: center;
    margin-bottom: 36px;
  }
  .kc-login-logo .brand {
    font-size: 28px;
    font-weight: 800;
    color: #0A1628;
    letter-spacing: 0.5px;
  }
  .kc-login-logo .brand span { color: #C9A84C; }
  .kc-login-logo .sub {
    font-size: 12px;
    color: #999;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
  }

  /* ---- Stat cards ---- */
  .kc-stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin: 24px 0;
  }
  .kc-stat {
    background: #fff;
    border-radius: 12px;
    padding: 22px 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border-left: 4px solid #C9A84C;
  }
  .kc-stat .label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #888;
    font-weight: 600;
    margin-bottom: 8px;
  }
  .kc-stat .value {
    font-size: 30px;
    font-weight: 700;
    color: #0A1628;
    line-height: 1;
  }
  .kc-stat .sub {
    font-size: 13px;
    color: #666;
    margin-top: 4px;
  }

  /* ---- Section cards ---- */
  .kc-card {
    background: #fff;
    border-radius: 12px;
    padding: 24px 28px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 20px;
  }
  .kc-section-title {
    font-size: 14px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #0A1628;
    padding-bottom: 12px;
    border-bottom: 2px solid #F0EAD6;
    margin-bottom: 18px;
  }
  .kc-section-title span { color: #C9A84C; }

  /* ---- Tabla de bonos ---- */
  .kc-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }
  .kc-table thead tr {
    background: #0A1628;
    color: #C9A84C;
  }
  .kc-table th {
    padding: 11px 14px;
    text-align: left;
    font-weight: 600;
    font-size: 11px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .kc-table tbody tr:nth-child(even) { background: #F7F8FC; }
  .kc-table tbody tr:hover { background: #FDF8EE; }
  .kc-table td {
    padding: 12px 14px;
    border-bottom: 1px solid #EEEEEE;
    color: #333;
  }
  .kc-monto { font-weight: 700; color: #1B6B35; }
  .kc-pw { font-family: monospace; background: #FFF8E7; padding: 3px 8px;
           border-radius: 4px; color: #7B5E07; font-size: 12px; }

  /* ---- Alertas ---- */
  .kc-alert-success {
    background: #EDFAF1; color: #1B6B35;
    border-left: 4px solid #1B6B35;
    padding: 10px 16px; border-radius: 7px;
    font-size: 14px; margin-bottom: 16px;
  }
  .kc-alert-danger {
    background: #FEECEC; color: #C0392B;
    border-left: 4px solid #C0392B;
    padding: 10px 16px; border-radius: 7px;
    font-size: 14px; margin-bottom: 16px;
  }

  /* ---- Empty state ---- */
  .kc-empty {
    text-align: center;
    padding: 48px 20px;
    color: #bbb;
  }
  .kc-empty .icon { font-size: 42px; display: block; margin-bottom: 10px; }
  .kc-empty p { font-size: 14px; }

  /* ---- Botones Streamlit ---- */
  .stButton > button {
    background: linear-gradient(135deg, #0A1628, #1A2F58) !important;
    color: #C9A84C !important;
    border: 1px solid #C9A84C !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 8px 20px !important;
    transition: all 0.2s !important;
  }
  .stButton > button:hover {
    background: #C9A84C !important;
    color: #0A1628 !important;
  }

  /* ---- Inputs ---- */
  .stTextInput > div > div > input,
  .stSelectbox > div > div,
  .stNumberInput > div > div > input,
  .stDateInput > div > div > input {
    border: 2px solid #e0e0e0 !important;
    border-radius: 8px !important;
  }
  .stTextInput > div > div > input:focus {
    border-color: #C9A84C !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.2) !important;
  }

  /* ---- Tabs ---- */
  .stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: transparent;
    border-bottom: 2px solid #E0D5B5;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #888;
    font-weight: 600;
    font-size: 13px;
    padding: 8px 22px;
    border-radius: 8px 8px 0 0;
  }
  .stTabs [aria-selected="true"] {
    background: #0A1628 !important;
    color: #C9A84C !important;
  }

  /* ---- Divider ---- */
  hr { border-color: #F0EAD6; }

  /* ---- Welcome banner ---- */
  .kc-welcome {
    background: linear-gradient(135deg, #0A1628 0%, #1A2F58 100%);
    border-radius: 12px;
    padding: 28px 32px;
    margin: 28px 0 24px 0;
    color: #fff;
    border-left: 5px solid #C9A84C;
  }
  .kc-welcome h2 { font-size: 22px; font-weight: 700; margin-bottom: 4px; }
  .kc-welcome h2 span { color: #C9A84C; }
  .kc-welcome p { color: rgba(255,255,255,0.6); font-size: 13px; }
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
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id   = None
    st.session_state.username  = ""
    st.session_state.nombre    = ""
    st.session_state.rol       = ""

# ---------------------------------------------------------------------------
# Navbar
# ---------------------------------------------------------------------------
def render_navbar():
    role_badge = ""
    user_info  = ""
    if st.session_state.logged_in:
        badge_color = "#C9A84C" if st.session_state.rol == "admin" else "rgba(255,255,255,0.2)"
        badge_text  = "ADMIN" if st.session_state.rol == "admin" else "USUARIO"
        role_badge  = f'<span class="kc-role-badge">{badge_text}</span>'
        user_info   = f'<span class="kc-user-chip">👤 {st.session_state.nombre}</span>'

    st.markdown(f"""
    <div class="kc-navbar">
      <div class="kc-navbar-brand">
        <div>
          <div class="kc-logo-text">KUNA <span>CAPITAL</span></div>
          <div class="kc-tagline">Portal de Bonos</div>
        </div>
      </div>
      <div class="kc-navbar-right">
        {user_info}
        {role_badge}
      </div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Vista: LOGIN
# ---------------------------------------------------------------------------
def view_login():
    render_navbar()
    st.markdown('<div style="height:60px"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown("""
        <div class="kc-login-card">
          <div class="kc-login-logo">
            <div class="brand">KUNA <span>CAPITAL</span></div>
            <div class="sub">Portal de Bonos</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.get("login_error"):
            st.error(st.session_state.login_error)
            st.session_state.login_error = ""

        with st.form("form_login", clear_on_submit=False):
            st.markdown("**Usuario**")
            username = st.text_input("Usuario", placeholder="Tu usuario", label_visibility="collapsed")
            st.markdown("**Contraseña**")
            password = st.text_input("Contraseña", type="password", placeholder="Tu contraseña", label_visibility="collapsed")
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Ingresar", use_container_width=True)

        if submitted:
            conn = get_db()
            user = conn.execute(
                "SELECT * FROM usuarios WHERE username = ? AND password = ?",
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
        <p style="text-align:center;color:#bbb;font-size:12px;margin-top:16px;">
          Acceso restringido &mdash; solo personal autorizado
        </p>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Vista: USUARIO
# ---------------------------------------------------------------------------
def view_usuario():
    render_navbar()

    conn  = get_db()
    bonos = conn.execute(
        "SELECT * FROM bonos WHERE usuario_id = ? ORDER BY fecha DESC",
        (st.session_state.user_id,),
    ).fetchall()
    conn.close()

    total_bonos  = len(bonos)
    total_monto  = sum(b["monto"] for b in bonos)
    ultimo_monto = bonos[0]["monto"] if bonos else 0
    ultimo_per   = bonos[0]["periodo"] if bonos else "-"

    st.markdown(f"""
    <div class="kc-welcome">
      <h2>Bienvenido, <span>{st.session_state.nombre}</span></h2>
      <p>Consulta el detalle de todos tus bonos registrados en Kuna Capital.</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kc-stat">
          <div class="label">Total bonos</div>
          <div class="value">{total_bonos}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kc-stat">
          <div class="label">Monto acumulado</div>
          <div class="value">${total_monto:,.2f}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kc-stat">
          <div class="label">Ultimo bono</div>
          <div class="value">${ultimo_monto:,.2f}</div>
          <div class="sub">{ultimo_per}</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""<div style="height:10px"></div>""", unsafe_allow_html=True)
        if st.button("Cerrar sesion", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="kc-section-title">MIS <span>BONOS</span></div>', unsafe_allow_html=True)

    if bonos:
        rows = "".join(f"""
          <tr>
            <td>{i+1}</td>
            <td>{b['concepto']}</td>
            <td>{b['periodo']}</td>
            <td>{b['fecha']}</td>
            <td class="kc-monto">${b['monto']:,.2f}</td>
          </tr>""" for i, b in enumerate(bonos))

        st.markdown(f"""
        <table class="kc-table">
          <thead>
            <tr>
              <th>#</th><th>Concepto</th><th>Periodo</th><th>Fecha</th><th>Monto</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="kc-empty">
          <span class="icon">📋</span>
          <p>No tienes bonos registrados aun.<br>Contacta a tu administrador.</p>
        </div>""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Vista: ADMINISTRADOR
# ---------------------------------------------------------------------------
def view_admin():
    render_navbar()

    conn     = get_db()
    usuarios = conn.execute("SELECT * FROM usuarios WHERE rol = 'usuario' ORDER BY nombre").fetchall()
    bonos    = conn.execute("""
        SELECT b.*, u.nombre as nombre_usuario, u.username
        FROM bonos b JOIN usuarios u ON b.usuario_id = u.id
        ORDER BY b.fecha DESC
    """).fetchall()
    conn.close()

    st.markdown(f"""
    <div class="kc-welcome">
      <h2>Panel de <span>Administrador</span></h2>
      <p>Gestiona usuarios y bonos del portal Kuna Capital.</p>
    </div>
    """, unsafe_allow_html=True)

    # Cerrar sesion arriba a la derecha
    col_sp, col_btn = st.columns([5, 1])
    with col_btn:
        if st.button("Cerrar sesion", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    # Mensajes
    if st.session_state.get("admin_msg"):
        msg, mtype = st.session_state.admin_msg
        if mtype == "success":
            st.markdown(f'<div class="kc-alert-success">✓ {msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="kc-alert-danger">✗ {msg}</div>', unsafe_allow_html=True)
        st.session_state.admin_msg = None

    tab_users, tab_bonos = st.tabs(["👥  Usuarios", "💰  Bonos"])

    # ---- TAB USUARIOS ----
    with tab_users:
        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("➕  Agregar nuevo usuario", expanded=True):
            with st.form("form_add_user", clear_on_submit=True):
                c1, c2, c3 = st.columns(3)
                with c1:
                    nombre   = st.text_input("Nombre completo", placeholder="Ej: Ana Lopez")
                with c2:
                    username = st.text_input("Username", placeholder="Ej: alopez")
                with c3:
                    password = st.text_input("Contrasena", placeholder="Contrasena inicial")
                submitted = st.form_submit_button("Agregar usuario", use_container_width=False)

            if submitted:
                if not all([nombre.strip(), username.strip(), password.strip()]):
                    st.session_state.admin_msg = ("Todos los campos son obligatorios.", "error")
                else:
                    try:
                        conn = get_db()
                        conn.execute(
                            "INSERT INTO usuarios (username, password, nombre, rol) VALUES (?, ?, ?, 'usuario')",
                            (username.strip(), password.strip(), nombre.strip()),
                        )
                        conn.commit()
                        conn.close()
                        st.session_state.admin_msg = (f"Usuario '{nombre.strip()}' creado exitosamente.", "success")
                    except sqlite3.IntegrityError:
                        st.session_state.admin_msg = (f"El username '{username.strip()}' ya existe.", "error")
                st.rerun()

        st.markdown('<div class="kc-section-title">USUARIOS REGISTRADOS — <span>CONTRASEÑAS VISIBLES</span></div>', unsafe_allow_html=True)

        if usuarios:
            rows = ""
            for u in usuarios:
                rows += f"""
                <tr>
                  <td>{u['id']}</td>
                  <td><strong>{u['nombre']}</strong></td>
                  <td>{u['username']}</td>
                  <td><span class="kc-pw">{u['password']}</span></td>
                </tr>"""
            st.markdown(f"""
            <table class="kc-table">
              <thead>
                <tr><th>ID</th><th>Nombre</th><th>Username</th><th>Contrasena</th></tr>
              </thead>
              <tbody>{rows}</tbody>
            </table>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Editar / Eliminar
            with st.expander("✏️  Editar o eliminar usuario"):
                user_opts = {f"{u['nombre']} ({u['username']})": u for u in usuarios}
                selected  = st.selectbox("Seleccionar usuario", list(user_opts.keys()))

                if selected:
                    u = user_opts[selected]
                    col_e, col_d = st.columns([2, 1])
                    with col_e:
                        with st.form("form_edit_user"):
                            new_nombre   = st.text_input("Nombre", value=u["nombre"])
                            new_password = st.text_input("Contrasena", value=u["password"])
                            if st.form_submit_button("Guardar cambios"):
                                conn = get_db()
                                conn.execute(
                                    "UPDATE usuarios SET nombre=?, password=? WHERE id=?",
                                    (new_nombre, new_password, u["id"]),
                                )
                                conn.commit()
                                conn.close()
                                st.session_state.admin_msg = ("Usuario actualizado.", "success")
                                st.rerun()
                    with col_d:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button(f"Eliminar a {u['nombre']}", type="primary"):
                            conn = get_db()
                            conn.execute("DELETE FROM bonos WHERE usuario_id = ?", (u["id"],))
                            conn.execute("DELETE FROM usuarios WHERE id = ?", (u["id"],))
                            conn.commit()
                            conn.close()
                            st.session_state.admin_msg = (f"Usuario '{u['nombre']}' eliminado.", "success")
                            st.rerun()
        else:
            st.markdown('<div class="kc-empty"><span class="icon">👥</span><p>No hay usuarios registrados aun.</p></div>', unsafe_allow_html=True)

    # ---- TAB BONOS ----
    with tab_bonos:
        st.markdown("<br>", unsafe_allow_html=True)

        if usuarios:
            with st.expander("➕  Agregar bono a un usuario", expanded=True):
                with st.form("form_add_bono", clear_on_submit=True):
                    c1, c2 = st.columns(2)
                    with c1:
                        user_opts_b  = {f"{u['nombre']} ({u['username']})": u["id"] for u in usuarios}
                        sel_user     = st.selectbox("Usuario", list(user_opts_b.keys()))
                        concepto     = st.text_input("Concepto", placeholder="Ej: Bono de desempeno Q1")
                    with c2:
                        monto  = st.number_input("Monto ($)", min_value=0.0, step=100.0, format="%.2f")
                        periodo= st.text_input("Periodo", placeholder="Ej: Q1 2024, Enero 2025")
                        fecha  = st.date_input("Fecha")

                    if st.form_submit_button("Agregar bono", use_container_width=False):
                        if not concepto.strip() or not periodo.strip():
                            st.session_state.admin_msg = ("Concepto y periodo son obligatorios.", "error")
                        else:
                            conn = get_db()
                            conn.execute(
                                "INSERT INTO bonos (usuario_id, concepto, monto, periodo, fecha) VALUES (?, ?, ?, ?, ?)",
                                (user_opts_b[sel_user], concepto.strip(), monto, periodo.strip(), str(fecha)),
                            )
                            conn.commit()
                            conn.close()
                            st.session_state.admin_msg = ("Bono agregado exitosamente.", "success")
                        st.rerun()
        else:
            st.info("Primero agrega usuarios para poder asignarles bonos.")

        st.markdown('<div class="kc-section-title">TODOS LOS <span>BONOS</span></div>', unsafe_allow_html=True)

        if bonos:
            rows = ""
            for b in bonos:
                rows += f"""
                <tr>
                  <td>{b['id']}</td>
                  <td>{b['nombre_usuario']}</td>
                  <td>{b['concepto']}</td>
                  <td>{b['periodo']}</td>
                  <td>{b['fecha']}</td>
                  <td class="kc-monto">${b['monto']:,.2f}</td>
                </tr>"""
            st.markdown(f"""
            <table class="kc-table">
              <thead>
                <tr><th>ID</th><th>Usuario</th><th>Concepto</th><th>Periodo</th><th>Fecha</th><th>Monto</th></tr>
              </thead>
              <tbody>{rows}</tbody>
            </table>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("🗑️  Eliminar bono"):
                bono_opts = {f"#{b['id']} — {b['nombre_usuario']} | {b['concepto']} | ${b['monto']:,.2f}": b["id"] for b in bonos}
                sel_bono  = st.selectbox("Seleccionar bono", list(bono_opts.keys()))
                if st.button("Eliminar bono seleccionado", type="primary"):
                    conn = get_db()
                    conn.execute("DELETE FROM bonos WHERE id = ?", (bono_opts[sel_bono],))
                    conn.commit()
                    conn.close()
                    st.session_state.admin_msg = ("Bono eliminado.", "success")
                    st.rerun()
        else:
            st.markdown('<div class="kc-empty"><span class="icon">💰</span><p>No hay bonos registrados aun.</p></div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Router principal
# ---------------------------------------------------------------------------
if not st.session_state.logged_in:
    view_login()
elif st.session_state.rol == "admin":
    view_admin()
else:
    view_usuario()
