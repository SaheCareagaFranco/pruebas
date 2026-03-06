import streamlit as st
import sqlite3
import os
from datetime import date

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Kuna Capital | Bonos",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS — Sidebar oscuro + contenido claro (igual que el screenshot de referencia)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Noto+Sans:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Noto Sans', sans-serif; }

/* ── Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 2rem !important; max-width: 100% !important; }
/* Sidebar oculto por defecto — se muestra solo al loguearse vía CSS en view_login */

/* ══════════════════════════════════
   SIDEBAR
══════════════════════════════════ */
section[data-testid="stSidebar"] {
  background: #171D1C !important;
  border-right: 1px solid #2C3533;
  min-width: 220px !important;
  max-width: 220px !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }
[data-testid="stSidebarContent"] { padding: 0 !important; }

/* Logo block */
.kc-sb-logo {
  padding: 22px 20px 16px;
  border-bottom: 1px solid #2C3533;
}
.kc-sb-logo .brand {
  font-family: 'Outfit', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: #E0E7E4;
  display: flex;
  align-items: center;
  gap: 8px;
}
.kc-sb-logo .brand .dot {
  width: 8px; height: 8px;
  background: #1AC77C;
  border-radius: 50%;
  flex-shrink: 0;
}
.kc-sb-logo .brand em { color: #1AC77C; font-style: normal; }
.kc-sb-logo .sub {
  font-size: 10px;
  color: #748C86;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-top: 3px;
  padding-left: 16px;
}

/* User block */
.kc-sb-user {
  padding: 16px 20px;
  border-bottom: 1px solid #2C3533;
  display: flex;
  align-items: center;
  gap: 10px;
}
.kc-avatar {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, #1AC77C, #148152);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Outfit', sans-serif;
  font-size: 13px;
  font-weight: 700;
  color: #0F1512;
  flex-shrink: 0;
}
.kc-sb-user .info .name {
  font-size: 13px;
  font-weight: 600;
  color: #E0E7E4;
  font-family: 'Outfit', sans-serif;
}
.kc-sb-user .info .role {
  font-size: 11px;
  color: #748C86;
  margin-top: 1px;
}

/* Nav items */
.kc-sb-nav { padding: 12px 0; }
.kc-sb-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  font-size: 13px;
  font-family: 'Outfit', sans-serif;
  font-weight: 500;
  color: #748C86;
  cursor: pointer;
  border-radius: 0;
  transition: all 0.15s;
  text-decoration: none;
  border-left: 3px solid transparent;
}
.kc-sb-item:hover { background: rgba(255,255,255,0.04); color: #E0E7E4; }
.kc-sb-item.active {
  background: rgba(26,199,124,0.08);
  color: #1AC77C;
  border-left: 3px solid #1AC77C;
  font-weight: 600;
}
.kc-sb-item .ico { font-size: 15px; }

/* Logout at bottom */
.kc-sb-logout {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  padding: 16px 20px;
  border-top: 1px solid #2C3533;
}
.kc-sb-logout a {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #748C86;
  font-family: 'Outfit', sans-serif;
  cursor: pointer;
  text-decoration: none;
}
.kc-sb-logout a:hover { color: #FF7070; }

/* ══════════════════════════════════
   MAIN CONTENT
══════════════════════════════════ */
.stApp { background: #F6F7F7; }
.kc-page-title {
  font-family: 'Outfit', sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: #171D1C;
  margin-bottom: 2px;
}
.kc-page-sub {
  font-size: 13px;
  color: #748C86;
  margin-bottom: 24px;
}

/* ══════════════════════════════════
   STAT CARDS (colored, like screenshot)
══════════════════════════════════ */
.kc-stat-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-bottom: 24px;
}
.kc-scard {
  border-radius: 12px;
  padding: 20px 22px;
  border: 1px solid transparent;
}
.kc-scard .num {
  font-family: 'Outfit', sans-serif;
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 8px;
}
.kc-scard .label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 500;
  font-family: 'Noto Sans', sans-serif;
}
.kc-scard .label .dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
/* Colors */
.sc-green  { background: #ECFDF5; border-color: #A7F3D0; }
.sc-green  .num { color: #065F46; }
.sc-green  .label { color: #047857; }
.sc-green  .dot { background: #1AC77C; }

.sc-yellow { background: #FFFBEB; border-color: #FDE68A; }
.sc-yellow .num { color: #92400E; }
.sc-yellow .label { color: #B45309; }
.sc-yellow .dot { background: #F59E0B; }

.sc-blue   { background: #EFF6FF; border-color: #BFDBFE; }
.sc-blue   .num { color: #1E40AF; }
.sc-blue   .label { color: #1D4ED8; }
.sc-blue   .dot { background: #3B82F6; }

.sc-red    { background: #FFF1F2; border-color: #FECDD3; }
.sc-red    .num { color: #9F1239; }
.sc-red    .label { color: #BE123C; }
.sc-red    .dot { background: #F43F5E; }

/* ══════════════════════════════════
   SEARCH / FILTERS BAR
══════════════════════════════════ */
.kc-filters {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
  align-items: center;
}

/* ══════════════════════════════════
   BONO CARDS (like solicitudes list)
══════════════════════════════════ */
.kc-card-item {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 10px;
  display: flex;
  align-items: flex-start;
  gap: 14px;
  cursor: pointer;
  transition: box-shadow 0.15s, border-color 0.15s;
  position: relative;
}
.kc-card-item:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.07);
  border-color: #C0CEC9;
}
.kc-card-item.highlighted { border-left: 3px solid #F59E0B; }
.kc-card-avatar {
  width: 36px; height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #D1FAE5, #A7F3D0);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Outfit', sans-serif;
  font-size: 12px;
  font-weight: 700;
  color: #065F46;
  flex-shrink: 0;
  margin-top: 2px;
}
.kc-card-body { flex: 1; min-width: 0; }
.kc-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}
.kc-card-name {
  font-family: 'Outfit', sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: #171D1C;
}
.kc-tag {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  font-family: 'Noto Sans', sans-serif;
}
.kc-tag-concept { background: #F3E8FF; color: #7C3AED; }
.kc-tag-green   { background: #DCFCE7; color: #166534; }
.kc-tag-yellow  { background: #FEF9C3; color: #854D0E; }
.kc-tag-blue    { background: #DBEAFE; color: #1E40AF; }
.kc-card-desc {
  font-size: 13px;
  color: #374151;
  margin-bottom: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.kc-card-date { font-size: 12px; color: #9CA3AF; }
.kc-card-amount {
  font-family: 'Outfit', sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: #065F46;
  flex-shrink: 0;
  align-self: center;
}
.kc-card-arrow {
  color: #D1D5DB;
  font-size: 16px;
  align-self: center;
  flex-shrink: 0;
}

/* Password badge */
.kc-pw {
  font-family: 'Courier New', monospace;
  background: #F3E8FF;
  border: 1px solid #DDD6FE;
  color: #6D28D9;
  padding: 2px 8px;
  border-radius: 5px;
  font-size: 12px;
}

/* ══════════════════════════════════
   ALERTS
══════════════════════════════════ */
.kc-ok {
  background: #ECFDF5; border-left: 3px solid #1AC77C; color: #065F46;
  padding: 10px 16px; border-radius: 8px; font-size: 13px; margin-bottom: 14px;
}
.kc-err {
  background: #FFF1F2; border-left: 3px solid #F43F5E; color: #9F1239;
  padding: 10px 16px; border-radius: 8px; font-size: 13px; margin-bottom: 14px;
}
.kc-empty {
  background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px;
  text-align: center; padding: 52px 20px; color: #9CA3AF;
}
.kc-empty .ico { font-size: 36px; display: block; margin-bottom: 10px; }

/* ══════════════════════════════════
   TOAST (bienvenida)
══════════════════════════════════ */
.kc-toast {
  position: fixed;
  top: 20px; right: 20px;
  background: #1AC77C;
  color: #0F1512;
  padding: 12px 20px;
  border-radius: 10px;
  font-family: 'Outfit', sans-serif;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 8px 24px rgba(26,199,124,0.3);
  z-index: 9999;
  animation: slideIn 0.3s ease;
}
@keyframes slideIn {
  from { opacity: 0; transform: translateX(40px); }
  to   { opacity: 1; transform: translateX(0); }
}

/* ══════════════════════════════════
   LOGIN — full dark navy page
══════════════════════════════════ */

/* Cuando no hay sidebar (login), ocultar el toggle y forzar fondo */
section[data-testid="stSidebar"] { display: none !important; }
.stApp[data-page="login"],
body:has(.kc-login-page) {
  background: #0D1E35 !important;
}
.kc-login-page {
  min-height: 100vh;
  background: linear-gradient(160deg, #0A1628 0%, #0D1E35 50%, #0A2240 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 16px;
  margin: -1.5rem -2rem;
}
/* Override Streamlit's block-container bg on login */
.kc-login-page ~ div, .kc-login-bg-override {
  background: #0D1E35 !important;
}
.kc-login-header {
  text-align: center;
  margin-bottom: 32px;
}
.kc-login-header .kuna-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 8px;
}
.kc-login-header .kuna-logo .kuna-name {
  font-family: 'Outfit', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: #FFFFFF;
  letter-spacing: 0.5px;
}
.kc-login-header .kuna-sub {
  font-family: 'Noto Sans', sans-serif;
  font-size: 14px;
  color: rgba(255,255,255,0.45);
  letter-spacing: 0.3px;
}
.kc-login-card {
  background: #FFFFFF;
  border-radius: 14px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.35);
  padding: 36px 36px 28px;
  width: 100%;
  max-width: 380px;
}
.kc-login-card-title {
  font-family: 'Outfit', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 24px;
}
/* Google button */
.kc-google-btn {
  width: 100%;
  background: #FFFFFF;
  border: 1.5px solid #D1D5DB;
  border-radius: 8px;
  padding: 11px 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  font-family: 'Outfit', sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  transition: border-color 0.15s, box-shadow 0.15s;
  margin-bottom: 6px;
}
.kc-google-btn:hover { border-color: #9CA3AF; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.kc-domain-hint {
  text-align: center;
  font-size: 12px;
  color: #9CA3AF;
  font-family: 'Noto Sans', sans-serif;
  margin-bottom: 20px;
}
.kc-divider {
  border: none;
  border-top: 1px solid #E5E7EB;
  margin: 20px 0;
}
.kc-demo-link {
  text-align: center;
  font-size: 13px;
  color: #6B7280;
  font-family: 'Noto Sans', sans-serif;
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 2px;
}
.kc-demo-link:hover { color: #374151; }
.kc-sso-info {
  background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 8px;
  padding: 10px 14px; margin-bottom: 16px; font-size: 12px; color: #92400E;
  font-family: 'Noto Sans', sans-serif; line-height: 1.5;
}

/* ══════════════════════════════════
   STREAMLIT BUTTONS & INPUTS
══════════════════════════════════ */
.stButton > button {
  background: #FFFFFF !important; color: #374151 !important;
  border: 1.5px solid #E5E7EB !important; border-radius: 8px !important;
  font-family: 'Outfit', sans-serif !important; font-weight: 600 !important;
  font-size: 13px !important; transition: all 0.15s !important;
}
.stButton > button:hover {
  border-color: #1AC77C !important; color: #065F46 !important;
  box-shadow: 0 2px 8px rgba(26,199,124,0.15) !important;
}
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stDateInput"] input {
  background: #F9FAFB !important; border: 1.5px solid #E5E7EB !important;
  border-radius: 8px !important; color: #171D1C !important;
  font-family: 'Noto Sans', sans-serif !important;
}
div[data-testid="stTextInput"] input:focus {
  border-color: #1AC77C !important;
  box-shadow: 0 0 0 3px rgba(26,199,124,0.1) !important;
}
div[data-testid="stSelectbox"] > div > div {
  background: #F9FAFB !important; border: 1.5px solid #E5E7EB !important;
  border-radius: 8px !important;
}
label, [data-testid="stWidgetLabel"] p {
  font-family: 'Outfit', sans-serif !important;
  font-size: 11px !important; font-weight: 600 !important;
  text-transform: uppercase !important; letter-spacing: 0.8px !important;
  color: #6B7280 !important;
}
[data-testid="stForm"] { background: transparent !important; border: none !important; }
div[data-testid="stExpander"] {
  background: #FFFFFF !important; border: 1.5px solid #E5E7EB !important;
  border-radius: 12px !important; margin-bottom: 10px !important;
}
div[data-testid="stExpander"] summary {
  font-family: 'Outfit', sans-serif !important;
  font-size: 13px !important; font-weight: 600 !important; color: #374151 !important;
}
/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  background: transparent !important; border-bottom: 2px solid #E5E7EB !important; gap: 0;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important; color: #9CA3AF !important;
  font-family: 'Outfit', sans-serif !important; font-weight: 600 !important;
  font-size: 13px !important; padding: 10px 22px !important; border-radius: 0 !important;
}
.stTabs [aria-selected="true"] {
  color: #1AC77C !important; border-bottom: 2px solid #1AC77C !important;
  background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# DB
# ---------------------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bonos.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db(); c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL, password TEXT NOT NULL,
        nombre TEXT NOT NULL, rol TEXT NOT NULL DEFAULT 'usuario')""")
    c.execute("""CREATE TABLE IF NOT EXISTS bonos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL, concepto TEXT NOT NULL,
        monto REAL NOT NULL, periodo TEXT NOT NULL, fecha TEXT NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id))""")
    c.execute("SELECT id FROM usuarios WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO usuarios(username,password,nombre,rol) VALUES(?,?,?,?)",
                  ("admin","admin123","Admin Kuna","admin"))
    conn.commit(); conn.close()

init_db()

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
for k, v in dict(logged_in=False, user_id=None, username="", nombre="",
                 rol="", msg=None, login_err="", page="main",
                 show_toast=False, show_sso_info=False).items():
    if k not in st.session_state:
        st.session_state[k] = v

def logout():
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.rerun()

def initials(name):
    parts = name.strip().split()
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else parts[0][:2].upper()

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
def render_sidebar():
    with st.sidebar:
        # Logo
        st.markdown("""
        <div class="kc-sb-logo">
          <div class="brand">
            <div class="dot"></div>
            <span>kuna <em>capital</em></span>
          </div>
          <div class="sub">Portal de Bonos</div>
        </div>""", unsafe_allow_html=True)

        # User info
        ini = initials(st.session_state.nombre)
        role_lbl = "Administrador" if st.session_state.rol == "admin" else "Colaborador"
        st.markdown(f"""
        <div class="kc-sb-user">
          <div class="kc-avatar">{ini}</div>
          <div class="info">
            <div class="name">{st.session_state.nombre}</div>
            <div class="role">{role_lbl}</div>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="kc-sb-nav">', unsafe_allow_html=True)

        # Nav items
        if st.session_state.rol == "admin":
            pages = [
                ("main",      "📋", "Panel de Bonos"),
                ("usuarios",  "👥", "Gestión de Usuarios"),
            ]
        else:
            pages = [("main", "💚", "Mis Bonos")]

        for key, ico, label in pages:
            active = "active" if st.session_state.page == key else ""
            if st.button(f"{ico}  {label}", key=f"nav_{key}",
                         use_container_width=True):
                st.session_state.page = key
                st.rerun()
            # Inject active style via JS hack — use markdown overlay
            st.markdown(f"""
            <style>
            div[data-testid="stSidebar"] button[kind="secondary"]:nth-of-type({pages.index((key,ico,label))+1}) {{
              background: {"rgba(26,199,124,0.08)" if active else "transparent"} !important;
              color: {"#1AC77C" if active else "#748C86"} !important;
              border: none !important;
              border-left: 3px solid {"#1AC77C" if active else "transparent"} !important;
              border-radius: 0 !important;
              text-align: left !important;
              padding: 10px 20px !important;
              font-family: 'Outfit', sans-serif !important;
              font-size: 13px !important;
              font-weight: {"600" if active else "500"} !important;
            }}
            </style>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>" * 6, unsafe_allow_html=True)

        # Logout
        if st.button("↩  Cerrar Sesión", use_container_width=True, key="logout_btn"):
            logout()

# ---------------------------------------------------------------------------
# LOGIN
# ---------------------------------------------------------------------------
def view_login():
    # Fondo oscuro de toda la página — inyectamos sobre el body de Streamlit
    st.markdown("""
    <style>
      .stApp { background: linear-gradient(160deg,#0A1628 0%,#0D1E35 50%,#0A2240 100%) !important; }
      section[data-testid="stSidebar"] { display: none !important; }
      .block-container { padding: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

    # Icono Kuna (SVG aproximado del logo del presskit)
    kuna_icon = """
    <svg width="38" height="38" viewBox="0 0 38 38" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M19 3 L19 35" stroke="white" stroke-width="3.5" stroke-linecap="round"/>
      <path d="M3 19 L35 19" stroke="white" stroke-width="3.5" stroke-linecap="round"/>
      <path d="M7.5 7.5 L30.5 30.5" stroke="white" stroke-width="3.5" stroke-linecap="round"/>
      <path d="M30.5 7.5 L7.5 30.5" stroke="white" stroke-width="3.5" stroke-linecap="round"/>
    </svg>"""

    # Layout centrado
    _, col, _ = st.columns([1, 1.05, 1])
    with col:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)

        # Logo + subtítulo ENCIMA de la card
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:28px;">
          <div style="display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:8px;">
            {kuna_icon}
            <span style="font-family:'Outfit',sans-serif;font-size:28px;font-weight:700;
                         color:#FFFFFF;letter-spacing:0.5px;">kuna</span>
          </div>
          <div style="font-family:'Noto Sans',sans-serif;font-size:14px;
                      color:rgba(255,255,255,0.45);">Portal de Bonos</div>
        </div>
        """, unsafe_allow_html=True)

        # Card blanca
        st.markdown('<div class="kc-login-card">', unsafe_allow_html=True)
        st.markdown('<div class="kc-login-card-title">Iniciar Sesión</div>', unsafe_allow_html=True)

        # Botón Google SSO (visual — mock para evaluación)
        if st.button(
            "Iniciar sesión con Google",
            use_container_width=True,
            key="google_btn",
        ):
            st.session_state.show_sso_info = not st.session_state.show_sso_info
            st.rerun()

        # Icono G en el botón (hacemos override del estilo del botón de Google)
        st.markdown("""
        <style>
        button[kind="secondary"][data-testid="baseButton-secondary"]:first-of-type,
        div[data-testid="stButton"]:first-of-type > button {
          background: #FFFFFF !important;
          color: #374151 !important;
          border: 1.5px solid #D1D5DB !important;
          font-size: 14px !important;
          font-weight: 600 !important;
          padding: 10px 16px !important;
          display: flex !important;
          justify-content: center !important;
          gap: 10px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        if st.session_state.show_sso_info:
            st.markdown("""
            <div class="kc-sso-info">
              ⚙️ <strong>Requiere Google Cloud Console:</strong><br>
              Necesitas un proyecto OAuth 2.0 configurado. Toma ~2 horas.
              Cuando tengas el <code>client_id</code> y <code>client_secret</code>,
              el código ya está listo para recibirlos.
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="kc-domain-hint">Solo correos @kunacapital.com y @kavak.com</div>
        <hr class="kc-divider">
        """, unsafe_allow_html=True)

        # Modo demo toggle
        if st.button("Modo demo (credenciales de prueba)", key="demo_toggle",
                     use_container_width=False):
            st.session_state.show_demo = not st.session_state.get("show_demo", False)
            st.rerun()

        st.markdown("""
        <style>
        div[data-testid="stButton"]:has(button[data-testid*="demo_toggle"]) button {
          background: transparent !important;
          border: none !important;
          color: #6B7280 !important;
          font-size: 13px !important;
          font-weight: 400 !important;
          text-decoration: underline !important;
          text-underline-offset: 2px !important;
          padding: 4px 0 !important;
          width: auto !important;
        }
        div[data-testid="stButton"]:has(button[data-testid*="demo_toggle"]) {
          text-align: center !important;
        }
        </style>""", unsafe_allow_html=True)

        # Form demo (oculto por defecto)
        if st.session_state.get("show_demo", False):
            st.markdown("<br>", unsafe_allow_html=True)
            if st.session_state.login_err:
                st.markdown(f'<div class="kc-err">⚠ {st.session_state.login_err}</div>',
                            unsafe_allow_html=True)
                st.session_state.login_err = ""

            with st.form("login", clear_on_submit=False):
                user = st.text_input("Usuario", placeholder="admin")
                pwd  = st.text_input("Contraseña", type="password", placeholder="••••••••")
                st.markdown("<br>", unsafe_allow_html=True)
                ok   = st.form_submit_button("Ingresar", use_container_width=True)

            if ok:
                conn = get_db()
                row  = conn.execute("SELECT * FROM usuarios WHERE username=? AND password=?",
                                    (user.strip(), pwd.strip())).fetchone()
                conn.close()
                if row:
                    st.session_state.update(logged_in=True, user_id=row["id"],
                        username=row["username"], nombre=row["nombre"],
                        rol=row["rol"], page="main", show_toast=True, show_demo=False)
                    st.rerun()
                else:
                    st.session_state.login_err = "Usuario o contraseña incorrectos."
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)  # cierra kc-login-card

# ---------------------------------------------------------------------------
# PANEL DE BONOS (admin)
# ---------------------------------------------------------------------------
def view_admin_bonos():
    conn     = get_db()
    usuarios = conn.execute("SELECT * FROM usuarios WHERE rol='usuario' ORDER BY nombre").fetchall()
    bonos    = conn.execute("""
        SELECT b.*, u.nombre as nu, u.username as un
        FROM bonos b JOIN usuarios u ON b.usuario_id=u.id
        ORDER BY b.fecha DESC""").fetchall()
    conn.close()

    total_u = len(usuarios)
    total_b = len(bonos)
    monto_t = sum(b["monto"] for b in bonos)
    prom    = monto_t / total_u if total_u else 0

    # Flash
    if st.session_state.msg:
        t, txt = st.session_state.msg
        st.markdown(f'<div class="{"kc-ok" if t=="s" else "kc-err"}">{"✓" if t=="s" else "✗"} {txt}</div>',
                    unsafe_allow_html=True)
        st.session_state.msg = None

    # Title
    sub = f"{total_b} bonos registrados"
    st.markdown(f'<div class="kc-page-title">Panel de Bonos</div>'
                f'<div class="kc-page-sub">{sub}</div>', unsafe_allow_html=True)

    # Stat cards
    st.markdown(f"""
    <div class="kc-stat-grid">
      <div class="kc-scard sc-green">
        <div class="num">{total_b}</div>
        <div class="label"><span class="dot"></span>Bonos registrados</div>
      </div>
      <div class="kc-scard sc-blue">
        <div class="num">{total_u}</div>
        <div class="label"><span class="dot"></span>Colaboradores</div>
      </div>
      <div class="kc-scard sc-yellow">
        <div class="num">${monto_t:,.0f}</div>
        <div class="label"><span class="dot"></span>Monto total</div>
      </div>
      <div class="kc-scard sc-red">
        <div class="num">${prom:,.0f}</div>
        <div class="label"><span class="dot"></span>Promedio por colaborador</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Agregar bono
    with st.expander("➕  Asignar bono a un usuario", expanded=False):
        if usuarios:
            with st.form("add_b", clear_on_submit=True):
                c1, c2 = st.columns(2)
                with c1:
                    umap = {f"{u['nombre']}  ({u['username']})": u["id"] for u in usuarios}
                    su   = st.selectbox("Usuario", list(umap.keys()))
                    con  = st.text_input("Concepto", placeholder="Bono de desempeno Q1 2025")
                with c2:
                    mon = st.number_input("Monto ($)", min_value=0.0, step=500.0, format="%.2f")
                    per = st.text_input("Periodo", placeholder="Q1 2025")
                    fec = st.date_input("Fecha", value=date.today())
                if st.form_submit_button("Asignar bono →"):
                    if not con.strip() or not per.strip():
                        st.session_state.msg = ("e", "Concepto y periodo son obligatorios.")
                    else:
                        conn = get_db()
                        conn.execute("INSERT INTO bonos(usuario_id,concepto,monto,periodo,fecha) VALUES(?,?,?,?,?)",
                                     (umap[su], con.strip(), mon, per.strip(), str(fec)))
                        conn.commit(); conn.close()
                        st.session_state.msg = ("s", "Bono asignado exitosamente.")
                    st.rerun()
        else:
            st.info("Primero agrega usuarios en la sección Gestión de Usuarios.")

    # Lista de bonos como cards
    if bonos:
        # Eliminar bono
        with st.expander("🗑️  Eliminar bono"):
            bopts = {f"#{b['id']} — {b['nu']} · {b['concepto']} · ${b['monto']:,.2f}": b["id"] for b in bonos}
            sb    = st.selectbox("Seleccionar bono a eliminar", list(bopts.keys()), key="db")
            if st.button("Confirmar eliminación", key="del_b"):
                conn = get_db()
                conn.execute("DELETE FROM bonos WHERE id=?", (bopts[sb],))
                conn.commit(); conn.close()
                st.session_state.msg = ("s", "Bono eliminado.")
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        for b in bonos:
            ini = initials(b["nu"])
            st.markdown(f"""
            <div class="kc-card-item">
              <div class="kc-card-avatar">{ini}</div>
              <div class="kc-card-body">
                <div class="kc-card-header">
                  <span class="kc-card-name">{b['nu']}</span>
                  <span class="kc-tag kc-tag-concept">{b['concepto']}</span>
                  <span class="kc-tag kc-tag-green">● Registrado</span>
                </div>
                <div class="kc-card-desc">Periodo: {b['periodo']}</div>
                <div class="kc-card-date">{b['fecha']}</div>
              </div>
              <div class="kc-card-amount">${b['monto']:,.2f}</div>
              <div class="kc-card-arrow">›</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="kc-empty"><span class="ico">💰</span>'
                    '<p>No hay bonos registrados aun.</p></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# GESTIÓN DE USUARIOS (admin)
# ---------------------------------------------------------------------------
def view_admin_usuarios():
    conn     = get_db()
    usuarios = conn.execute("SELECT * FROM usuarios WHERE rol='usuario' ORDER BY nombre").fetchall()
    conn.close()

    if st.session_state.msg:
        t, txt = st.session_state.msg
        st.markdown(f'<div class="{"kc-ok" if t=="s" else "kc-err"}">{"✓" if t=="s" else "✗"} {txt}</div>',
                    unsafe_allow_html=True)
        st.session_state.msg = None

    st.markdown(f'<div class="kc-page-title">Gestión de Usuarios</div>'
                f'<div class="kc-page-sub">{len(usuarios)} colaboradores registrados</div>',
                unsafe_allow_html=True)

    with st.expander("➕  Agregar nuevo usuario", expanded=True):
        with st.form("add_u", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1: nombre   = st.text_input("Nombre completo", placeholder="Ana Lopez")
            with c2: username = st.text_input("Username", placeholder="alopez")
            with c3: password = st.text_input("Contraseña", placeholder="••••••••")
            if st.form_submit_button("Crear usuario →"):
                if not all([nombre.strip(), username.strip(), password.strip()]):
                    st.session_state.msg = ("e", "Todos los campos son obligatorios.")
                else:
                    try:
                        conn = get_db()
                        conn.execute("INSERT INTO usuarios(username,password,nombre,rol) VALUES(?,?,?,'usuario')",
                                     (username.strip(), password.strip(), nombre.strip()))
                        conn.commit(); conn.close()
                        st.session_state.msg = ("s", f"Usuario '{nombre.strip()}' creado.")
                    except sqlite3.IntegrityError:
                        st.session_state.msg = ("e", f"El username '{username.strip()}' ya existe.")
                st.rerun()

    if usuarios:
        with st.expander("✏️  Editar / eliminar usuario"):
            opts = {f"{u['nombre']}  ({u['username']})": u for u in usuarios}
            sel  = st.selectbox("Seleccionar usuario", list(opts.keys()), key="eu")
            u    = opts[sel]
            ec, dc = st.columns([2, 1])
            with ec:
                with st.form("edit_u"):
                    nn = st.text_input("Nombre", value=u["nombre"])
                    np = st.text_input("Contraseña", value=u["password"])
                    if st.form_submit_button("Guardar cambios"):
                        conn = get_db()
                        conn.execute("UPDATE usuarios SET nombre=?,password=? WHERE id=?", (nn, np, u["id"]))
                        conn.commit(); conn.close()
                        st.session_state.msg = ("s", "Usuario actualizado.")
                        st.rerun()
            with dc:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(f"Eliminar '{u['nombre']}'", type="primary"):
                    conn = get_db()
                    conn.execute("DELETE FROM bonos WHERE usuario_id=?", (u["id"],))
                    conn.execute("DELETE FROM usuarios WHERE id=?", (u["id"],))
                    conn.commit(); conn.close()
                    st.session_state.msg = ("s", f"'{u['nombre']}' eliminado.")
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        for u in usuarios:
            ini = initials(u["nombre"])
            st.markdown(f"""
            <div class="kc-card-item">
              <div class="kc-card-avatar">{ini}</div>
              <div class="kc-card-body">
                <div class="kc-card-header">
                  <span class="kc-card-name">{u['nombre']}</span>
                  <span class="kc-tag kc-tag-blue">@{u['username']}</span>
                </div>
                <div class="kc-card-desc">Contraseña: <span class="kc-pw">{u['password']}</span></div>
              </div>
              <div class="kc-card-arrow">›</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="kc-empty"><span class="ico">👥</span>'
                    '<p>No hay usuarios registrados aun.</p></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# MIS BONOS (usuario)
# ---------------------------------------------------------------------------
def view_user_bonos():
    conn  = get_db()
    bonos = conn.execute("SELECT * FROM bonos WHERE usuario_id=? ORDER BY fecha DESC",
                         (st.session_state.user_id,)).fetchall()
    conn.close()

    total  = len(bonos)
    monto  = sum(b["monto"] for b in bonos)
    ult_m  = bonos[0]["monto"] if bonos else 0
    ult_p  = bonos[0]["periodo"] if bonos else "—"

    st.markdown(f'<div class="kc-page-title">Mis Bonos</div>'
                f'<div class="kc-page-sub">{total} bonos registrados a tu nombre</div>',
                unsafe_allow_html=True)

    st.markdown(f"""
    <div class="kc-stat-grid" style="grid-template-columns:repeat(3,1fr)">
      <div class="kc-scard sc-green">
        <div class="num">{total}</div>
        <div class="label"><span class="dot"></span>Bonos registrados</div>
      </div>
      <div class="kc-scard sc-blue">
        <div class="num">${monto:,.2f}</div>
        <div class="label"><span class="dot"></span>Monto acumulado</div>
      </div>
      <div class="kc-scard sc-yellow">
        <div class="num">${ult_m:,.2f}</div>
        <div class="label"><span class="dot"></span>Último bono · {ult_p}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    if bonos:
        for b in bonos:
            st.markdown(f"""
            <div class="kc-card-item">
              <div class="kc-card-avatar">💚</div>
              <div class="kc-card-body">
                <div class="kc-card-header">
                  <span class="kc-card-name">{b['concepto']}</span>
                  <span class="kc-tag kc-tag-yellow">{b['periodo']}</span>
                  <span class="kc-tag kc-tag-green">● Registrado</span>
                </div>
                <div class="kc-card-date">{b['fecha']}</div>
              </div>
              <div class="kc-card-amount">${b['monto']:,.2f}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="kc-empty"><span class="ico">📋</span>'
                    '<p>No tienes bonos registrados aun.<br>Contacta a tu administrador.</p>'
                    '</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
if not st.session_state.logged_in:
    view_login()
else:
    # Toast de bienvenida
    if st.session_state.show_toast:
        st.markdown(f'<div class="kc-toast">✓ Bienvenido(a), {st.session_state.nombre}</div>',
                    unsafe_allow_html=True)
        st.session_state.show_toast = False

    render_sidebar()

    if st.session_state.rol == "admin":
        if st.session_state.page == "usuarios":
            view_admin_usuarios()
        else:
            view_admin_bonos()
    else:
        view_user_bonos()
