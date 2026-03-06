import streamlit as st
import sqlite3
import os

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Kuna Capital | Bonos",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# CSS — Dark premium theme (Kuna Capital)
# Outfit (headings) + Noto Sans (body)
# Colors: bg #171D1C · card #2C3533 · green #1AC77C · navy #002236
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Noto+Sans:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
  font-family: 'Noto Sans', sans-serif;
}

/* ── Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #1E2423; }
::-webkit-scrollbar-thumb { background: #3A4542; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #1AC77C; }

/* ══════════════════════════════════════════
   NAVBAR
══════════════════════════════════════════ */
.kc-nav {
  background: #0F1512;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  border-bottom: 1px solid #2C3533;
  position: sticky;
  top: 0;
  z-index: 999;
}
.kc-nav-logo {
  display: flex;
  align-items: center;
  gap: 10px;
}
.kc-nav-logo .pulse {
  width: 8px; height: 8px;
  background: #1AC77C;
  border-radius: 50%;
  box-shadow: 0 0 0 3px rgba(26,199,124,0.2);
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%,100% { box-shadow: 0 0 0 3px rgba(26,199,124,0.2); }
  50%      { box-shadow: 0 0 0 6px rgba(26,199,124,0.05); }
}
.kc-nav-logo .wordmark {
  font-family: 'Outfit', sans-serif;
  font-size: 17px;
  font-weight: 700;
  color: #E0E7E4;
  letter-spacing: 0.3px;
}
.kc-nav-logo .wordmark em {
  color: #1AC77C;
  font-style: normal;
}
.kc-nav-logo .sep {
  width: 1px; height: 18px;
  background: #3A4542;
  margin: 0 10px;
}
.kc-nav-logo .module {
  font-size: 11px;
  color: #748C86;
  letter-spacing: 2px;
  text-transform: uppercase;
  font-family: 'Noto Sans', sans-serif;
}
.kc-nav-right { display: flex; align-items: center; gap: 10px; }
.kc-pill {
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-family: 'Outfit', sans-serif;
  font-weight: 500;
}
.kc-pill-user {
  background: rgba(26,199,124,0.08);
  border: 1px solid rgba(26,199,124,0.2);
  color: #1AC77C;
}
.kc-pill-admin {
  background: #1AC77C;
  color: #0F1512;
  font-weight: 700;
  letter-spacing: 0.5px;
}

/* ══════════════════════════════════════════
   PAGE WRAPPER
══════════════════════════════════════════ */
.kc-page { max-width: 1180px; margin: 0 auto; padding: 36px 32px 60px; }

/* ══════════════════════════════════════════
   HERO BANNER
══════════════════════════════════════════ */
.kc-hero {
  background: linear-gradient(135deg, #002236 0%, #00304C 100%);
  border-radius: 16px;
  padding: 36px 40px;
  margin-bottom: 28px;
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(26,199,124,0.15);
}
.kc-hero::before {
  content: '';
  position: absolute; top: -80px; right: -60px;
  width: 260px; height: 260px;
  background: radial-gradient(circle, rgba(26,199,124,0.12) 0%, transparent 70%);
  border-radius: 50%;
}
.kc-hero::after {
  content: '';
  position: absolute; bottom: -100px; left: 30%;
  width: 320px; height: 320px;
  background: radial-gradient(circle, rgba(0,116,180,0.08) 0%, transparent 70%);
  border-radius: 50%;
}
.kc-hero-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(26,199,124,0.12);
  border: 1px solid rgba(26,199,124,0.25);
  color: #1AC77C;
  font-size: 11px;
  font-family: 'Outfit', sans-serif;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  padding: 4px 12px;
  border-radius: 8px;
  margin-bottom: 14px;
}
.kc-hero h1 {
  font-family: 'Outfit', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: #FFFFFF;
  margin-bottom: 6px;
  position: relative;
  z-index: 1;
}
.kc-hero h1 em { color: #1AC77C; font-style: normal; }
.kc-hero p {
  color: #748C86;
  font-size: 14px;
  position: relative;
  z-index: 1;
}

/* ══════════════════════════════════════════
   STAT CARDS
══════════════════════════════════════════ */
.kc-stat {
  background: #2C3533;
  border-radius: 14px;
  padding: 22px 22px 20px;
  border: 1px solid #3A4542;
  position: relative;
  overflow: hidden;
  transition: border-color 0.2s;
}
.kc-stat:hover { border-color: rgba(26,199,124,0.4); }
.kc-stat::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, #1AC77C, #1DE08C);
}
.kc-stat .ico {
  font-size: 20px;
  margin-bottom: 12px;
  display: block;
}
.kc-stat .lbl {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: #748C86;
  font-family: 'Outfit', sans-serif;
  font-weight: 600;
  margin-bottom: 8px;
}
.kc-stat .val {
  font-family: 'Outfit', sans-serif;
  font-size: 26px;
  font-weight: 700;
  color: #E0E7E4;
  line-height: 1;
}
.kc-stat .sub {
  font-size: 11px;
  color: #748C86;
  margin-top: 5px;
}

/* ══════════════════════════════════════════
   SECTION TITLE
══════════════════════════════════════════ */
.kc-stitle {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: 'Outfit', sans-serif;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: #748C86;
  margin: 28px 0 14px;
}
.kc-stitle::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #2C3533;
}
.kc-stitle em { color: #1AC77C; font-style: normal; }

/* ══════════════════════════════════════════
   TABLE
══════════════════════════════════════════ */
.kc-tbl {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Noto Sans', sans-serif;
  font-size: 13px;
  background: #2C3533;
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid #3A4542;
}
.kc-tbl thead tr { background: #222926; }
.kc-tbl th {
  padding: 13px 18px;
  text-align: left;
  font-size: 10px;
  font-family: 'Outfit', sans-serif;
  font-weight: 700;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  color: #748C86;
  border-bottom: 1px solid #3A4542;
}
.kc-tbl td {
  padding: 14px 18px;
  border-bottom: 1px solid #323D3A;
  color: #C0CEC9;
}
.kc-tbl tr:last-child td { border-bottom: none; }
.kc-tbl tbody tr:hover td {
  background: rgba(26,199,124,0.04);
  color: #E0E7E4;
}
.kc-val { font-weight: 600; color: #1AC77C !important; font-family: 'Outfit', sans-serif; }
.kc-name { color: #E0E7E4 !important; font-weight: 500; }
.kc-pw {
  font-family: 'Courier New', monospace;
  background: rgba(26,199,124,0.08);
  border: 1px solid rgba(26,199,124,0.15);
  color: #1AC77C;
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 12px;
  letter-spacing: 0.5px;
}

/* ══════════════════════════════════════════
   ALERTS
══════════════════════════════════════════ */
.kc-ok {
  background: rgba(26,199,124,0.08);
  border: 1px solid rgba(26,199,124,0.2);
  border-left: 3px solid #1AC77C;
  color: #1AC77C;
  padding: 10px 16px;
  border-radius: 10px;
  font-size: 13px;
  margin-bottom: 16px;
}
.kc-err {
  background: rgba(220,50,50,0.06);
  border: 1px solid rgba(220,50,50,0.15);
  border-left: 3px solid #DC3232;
  color: #FF7070;
  padding: 10px 16px;
  border-radius: 10px;
  font-size: 13px;
  margin-bottom: 16px;
}
.kc-empty {
  text-align: center;
  padding: 52px 20px;
  color: #485856;
  background: #2C3533;
  border-radius: 14px;
  border: 1px solid #3A4542;
}
.kc-empty .ico { font-size: 38px; display: block; margin-bottom: 12px; }
.kc-empty p { font-size: 14px; color: #748C86; line-height: 1.6; }

/* ══════════════════════════════════════════
   LOGIN
══════════════════════════════════════════ */
.kc-login-outer {
  min-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 16px;
}
.kc-login-card {
  background: #2C3533;
  border-radius: 20px;
  border: 1px solid #3A4542;
  padding: 52px 44px 40px;
  width: 100%;
  max-width: 400px;
  position: relative;
  overflow: hidden;
}
.kc-login-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, #1AC77C, #1DE08C, rgba(26,199,124,0));
}
.kc-login-brand {
  text-align: center;
  margin-bottom: 36px;
}
.kc-login-brand .wordmark {
  font-family: 'Outfit', sans-serif;
  font-size: 30px;
  font-weight: 800;
  color: #E0E7E4;
  letter-spacing: 1px;
  line-height: 1;
}
.kc-login-brand .wordmark em { color: #1AC77C; font-style: normal; }
.kc-login-brand .sub {
  font-size: 10px;
  font-family: 'Outfit', sans-serif;
  font-weight: 500;
  color: #748C86;
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-top: 8px;
}
.kc-login-brand .bar {
  width: 32px; height: 2px;
  background: #1AC77C;
  border-radius: 1px;
  margin: 12px auto 0;
}
.kc-login-footer {
  text-align: center;
  color: #485856;
  font-size: 11px;
  margin-top: 20px;
  font-family: 'Noto Sans', sans-serif;
  letter-spacing: 0.3px;
}

/* ══════════════════════════════════════════
   STREAMLIT OVERRIDES
══════════════════════════════════════════ */
/* Buttons */
.stButton > button {
  background: transparent !important;
  color: #1AC77C !important;
  border: 1.5px solid #1AC77C !important;
  border-radius: 8px !important;
  font-family: 'Outfit', sans-serif !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  letter-spacing: 0.3px !important;
  padding: 8px 20px !important;
  transition: all 0.15s ease !important;
}
.stButton > button:hover {
  background: #1AC77C !important;
  color: #0F1512 !important;
}

/* Inputs */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
  background: #222926 !important;
  border: 1.5px solid #3A4542 !important;
  border-radius: 8px !important;
  color: #E0E7E4 !important;
  font-family: 'Noto Sans', sans-serif !important;
  font-size: 14px !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {
  border-color: #1AC77C !important;
  box-shadow: 0 0 0 3px rgba(26,199,124,0.1) !important;
}

/* Date input */
div[data-testid="stDateInput"] input {
  background: #222926 !important;
  border: 1.5px solid #3A4542 !important;
  border-radius: 8px !important;
  color: #E0E7E4 !important;
}

/* Selectbox */
div[data-testid="stSelectbox"] > div > div {
  background: #222926 !important;
  border: 1.5px solid #3A4542 !important;
  border-radius: 8px !important;
  color: #E0E7E4 !important;
}

/* Labels */
label, .stTextInput label p, .stSelectbox label p,
.stNumberInput label p, .stDateInput label p,
[data-testid="stWidgetLabel"] p {
  font-family: 'Outfit', sans-serif !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 1px !important;
  color: #748C86 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  background: transparent !important;
  gap: 2px;
  border-bottom: 1px solid #2C3533 !important;
  padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: #748C86 !important;
  font-family: 'Outfit', sans-serif !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  padding: 10px 22px !important;
  border-radius: 8px 8px 0 0 !important;
  letter-spacing: 0.3px !important;
  border: none !important;
}
.stTabs [aria-selected="true"] {
  background: rgba(26,199,124,0.1) !important;
  color: #1AC77C !important;
  border-bottom: 2px solid #1AC77C !important;
}

/* Expander */
div[data-testid="stExpander"] {
  background: #2C3533 !important;
  border: 1px solid #3A4542 !important;
  border-radius: 12px !important;
  margin-bottom: 12px !important;
}
div[data-testid="stExpander"] summary {
  font-family: 'Outfit', sans-serif !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  color: #C0CEC9 !important;
}
div[data-testid="stExpander"] summary:hover { color: #1AC77C !important; }

/* Form border */
[data-testid="stForm"] {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
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
    conn = get_db()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        nombre TEXT NOT NULL,
        rol TEXT NOT NULL DEFAULT 'usuario'
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS bonos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        concepto TEXT NOT NULL,
        monto REAL NOT NULL,
        periodo TEXT NOT NULL,
        fecha TEXT NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )""")
    c.execute("SELECT id FROM usuarios WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO usuarios (username,password,nombre,rol) VALUES(?,?,?,?)",
                  ("admin","admin123","Administrador","admin"))
    conn.commit(); conn.close()

init_db()

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
for k, v in dict(logged_in=False, user_id=None, username="",
                 nombre="", rol="", msg=None, login_err="").items():
    if k not in st.session_state:
        st.session_state[k] = v

def logout():
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.rerun()

# ---------------------------------------------------------------------------
# Navbar
# ---------------------------------------------------------------------------
def navbar():
    right = ""
    if st.session_state.logged_in:
        cls = "kc-pill-admin" if st.session_state.rol == "admin" else "kc-pill-user"
        tag = "ADMIN" if st.session_state.rol == "admin" else "USUARIO"
        right = f'<span class="kc-pill kc-pill-user" style="margin-right:4px">👤 {st.session_state.nombre}</span><span class="kc-pill {cls}">{tag}</span>'
    st.markdown(f"""
    <div class="kc-nav">
      <div class="kc-nav-logo">
        <div class="pulse"></div>
        <span class="wordmark">KUNA <em>CAPITAL</em></span>
        <div class="sep"></div>
        <span class="module">Portal de Bonos</span>
      </div>
      <div class="kc-nav-right">{right}</div>
    </div>""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# LOGIN
# ---------------------------------------------------------------------------
def view_login():
    navbar()
    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        st.markdown('<div style="height:48px"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="kc-login-card">
          <div class="kc-login-brand">
            <div class="wordmark">KUNA <em>CAPITAL</em></div>
            <div class="sub">Portal de Bonos</div>
            <div class="bar"></div>
          </div>
        </div>""", unsafe_allow_html=True)

        if st.session_state.login_err:
            st.markdown(f'<div class="kc-err">⚠ {st.session_state.login_err}</div>',
                        unsafe_allow_html=True)
            st.session_state.login_err = ""

        with st.form("login", clear_on_submit=False):
            user = st.text_input("Usuario", placeholder="tu.usuario")
            pwd  = st.text_input("Contraseña", type="password", placeholder="••••••••")
            st.markdown("<br>", unsafe_allow_html=True)
            ok   = st.form_submit_button("Ingresar →", use_container_width=True)

        if ok:
            conn = get_db()
            row = conn.execute("SELECT * FROM usuarios WHERE username=? AND password=?",
                               (user.strip(), pwd.strip())).fetchone()
            conn.close()
            if row:
                st.session_state.update(logged_in=True, user_id=row["id"],
                    username=row["username"], nombre=row["nombre"], rol=row["rol"])
                st.rerun()
            else:
                st.session_state.login_err = "Usuario o contraseña incorrectos."
                st.rerun()

        st.markdown('<p class="kc-login-footer">Acceso restringido · Solo personal autorizado</p>',
                    unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# USUARIO
# ---------------------------------------------------------------------------
def view_usuario():
    navbar()
    st.markdown('<div class="kc-page">', unsafe_allow_html=True)

    conn  = get_db()
    bonos = conn.execute(
        "SELECT * FROM bonos WHERE usuario_id=? ORDER BY fecha DESC",
        (st.session_state.user_id,)).fetchall()
    conn.close()

    total  = len(bonos)
    monto  = sum(b["monto"] for b in bonos)
    ult_m  = bonos[0]["monto"] if bonos else 0
    ult_p  = bonos[0]["periodo"] if bonos else "—"

    # Hero
    st.markdown(f"""
    <div class="kc-hero">
      <div class="kc-hero-tag">
        <span>●</span> Mi portal
      </div>
      <h1>Hola, <em>{st.session_state.nombre}</em> 👋</h1>
      <p>Aqui puedes consultar todos tus bonos registrados en Kuna Capital.</p>
    </div>""", unsafe_allow_html=True)

    # Stats
    c1, c2, c3, c_btn = st.columns([1, 1, 1, 0.55])
    with c1:
        st.markdown(f"""<div class="kc-stat">
          <span class="ico">🧾</span>
          <div class="lbl">Bonos registrados</div>
          <div class="val">{total}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kc-stat">
          <span class="ico">💰</span>
          <div class="lbl">Monto acumulado</div>
          <div class="val">${monto:,.2f}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kc-stat">
          <span class="ico">📅</span>
          <div class="lbl">Ultimo bono</div>
          <div class="val">${ult_m:,.2f}</div>
          <div class="sub">{ult_p}</div>
        </div>""", unsafe_allow_html=True)
    with c_btn:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Cerrar sesion", use_container_width=True):
            logout()

    # Tabla
    st.markdown('<div class="kc-stitle"><em>MIS</em> BONOS</div>', unsafe_allow_html=True)

    if bonos:
        rows = "".join(f"""<tr>
          <td style="color:#748C86;font-size:12px">{i+1}</td>
          <td class="kc-name">{b['concepto']}</td>
          <td>{b['periodo']}</td>
          <td>{b['fecha']}</td>
          <td class="kc-val">${b['monto']:,.2f}</td>
        </tr>""" for i, b in enumerate(bonos))
        st.markdown(f"""<table class="kc-tbl">
          <thead><tr><th>#</th><th>Concepto</th><th>Periodo</th><th>Fecha</th><th>Monto</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="kc-empty">
          <span class="ico">📋</span>
          <p>No tienes bonos registrados aun.<br>Contacta a tu administrador.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# ADMIN
# ---------------------------------------------------------------------------
def view_admin():
    navbar()
    st.markdown('<div class="kc-page">', unsafe_allow_html=True)

    conn     = get_db()
    usuarios = conn.execute("SELECT * FROM usuarios WHERE rol='usuario' ORDER BY nombre").fetchall()
    bonos    = conn.execute("""
        SELECT b.*, u.nombre as nu, u.username as un
        FROM bonos b JOIN usuarios u ON b.usuario_id=u.id
        ORDER BY b.fecha DESC""").fetchall()
    conn.close()

    # Hero + logout
    hcol, bcol = st.columns([5, 0.8])
    with hcol:
        st.markdown("""<div class="kc-hero">
          <div class="kc-hero-tag"><span>⚙</span> Administrador</div>
          <h1>Panel de <em>Administracion</em></h1>
          <p>Gestiona usuarios, asigna bonos y consulta credenciales.</p>
        </div>""", unsafe_allow_html=True)
    with bcol:
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        if st.button("Cerrar sesion", use_container_width=True):
            logout()

    # Flash messages
    if st.session_state.msg:
        txt, t = st.session_state.msg
        st.markdown(f'<div class="{"kc-ok" if t=="s" else "kc-err"}">{"✓" if t=="s" else "✗"} {txt}</div>',
                    unsafe_allow_html=True)
        st.session_state.msg = None

    tab_u, tab_b = st.tabs(["  👥  Usuarios  ", "  💰  Bonos  "])

    # ── USUARIOS ──────────────────────────────────────────────────────────────
    with tab_u:
        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("➕  Agregar nuevo usuario", expanded=True):
            with st.form("add_u", clear_on_submit=True):
                c1, c2, c3 = st.columns(3)
                with c1: nombre   = st.text_input("Nombre completo", placeholder="Ana Lopez")
                with c2: username = st.text_input("Username", placeholder="alopez")
                with c3: password = st.text_input("Contraseña", placeholder="••••••••")
                if st.form_submit_button("Crear usuario →"):
                    if not all([nombre.strip(), username.strip(), password.strip()]):
                        st.session_state.msg = ("Todos los campos son obligatorios.", "e")
                    else:
                        try:
                            conn = get_db()
                            conn.execute("INSERT INTO usuarios(username,password,nombre,rol) VALUES(?,?,?,'usuario')",
                                         (username.strip(), password.strip(), nombre.strip()))
                            conn.commit(); conn.close()
                            st.session_state.msg = (f"Usuario '{nombre.strip()}' creado exitosamente.", "s")
                        except sqlite3.IntegrityError:
                            st.session_state.msg = (f"El username '{username.strip()}' ya existe.", "e")
                    st.rerun()

        st.markdown('<div class="kc-stitle"><em>USUARIOS</em> REGISTRADOS — CONTRASEÑAS VISIBLES</div>',
                    unsafe_allow_html=True)

        if usuarios:
            rows = "".join(f"""<tr>
              <td style="color:#748C86;font-size:12px">{u['id']}</td>
              <td class="kc-name">{u['nombre']}</td>
              <td style="color:#C0CEC9">{u['username']}</td>
              <td><span class="kc-pw">{u['password']}</span></td>
            </tr>""" for u in usuarios)
            st.markdown(f"""<table class="kc-tbl">
              <thead><tr><th>ID</th><th>Nombre</th><th>Username</th><th>Contraseña</th></tr></thead>
              <tbody>{rows}</tbody>
            </table>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("✏️  Editar / eliminar usuario"):
                opts = {f"{u['nombre']}  ({u['username']})": u for u in usuarios}
                sel  = st.selectbox("Seleccionar", list(opts.keys()), key="eu")
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
                            st.session_state.msg = ("Usuario actualizado.", "s")
                            st.rerun()
                with dc:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button(f"Eliminar '{u['nombre']}'", type="primary"):
                        conn = get_db()
                        conn.execute("DELETE FROM bonos WHERE usuario_id=?", (u["id"],))
                        conn.execute("DELETE FROM usuarios WHERE id=?", (u["id"],))
                        conn.commit(); conn.close()
                        st.session_state.msg = (f"'{u['nombre']}' eliminado.", "s")
                        st.rerun()
        else:
            st.markdown('<div class="kc-empty"><span class="ico">👥</span><p>No hay usuarios aun.</p></div>',
                        unsafe_allow_html=True)

    # ── BONOS ─────────────────────────────────────────────────────────────────
    with tab_b:
        st.markdown("<br>", unsafe_allow_html=True)

        if usuarios:
            with st.expander("➕  Asignar bono a un usuario", expanded=True):
                with st.form("add_b", clear_on_submit=True):
                    r1, r2 = st.columns(2)
                    with r1:
                        umap = {f"{u['nombre']}  ({u['username']})": u["id"] for u in usuarios}
                        su   = st.selectbox("Usuario", list(umap.keys()))
                        con  = st.text_input("Concepto", placeholder="Bono de desempeno Q1 2025")
                    with r2:
                        mon  = st.number_input("Monto ($)", min_value=0.0, step=500.0, format="%.2f")
                        per  = st.text_input("Periodo", placeholder="Q1 2025")
                        fec  = st.date_input("Fecha")
                    if st.form_submit_button("Asignar bono →"):
                        if not con.strip() or not per.strip():
                            st.session_state.msg = ("Concepto y periodo son obligatorios.", "e")
                        else:
                            conn = get_db()
                            conn.execute("INSERT INTO bonos(usuario_id,concepto,monto,periodo,fecha) VALUES(?,?,?,?,?)",
                                         (umap[su], con.strip(), mon, per.strip(), str(fec)))
                            conn.commit(); conn.close()
                            st.session_state.msg = ("Bono asignado exitosamente.", "s")
                        st.rerun()
        else:
            st.markdown('<div class="kc-empty"><span class="ico">👥</span><p>Primero agrega usuarios.</p></div>',
                        unsafe_allow_html=True)

        st.markdown('<div class="kc-stitle">TODOS LOS <em>BONOS</em></div>', unsafe_allow_html=True)

        if bonos:
            rows = "".join(f"""<tr>
              <td style="color:#748C86;font-size:12px">{b['id']}</td>
              <td class="kc-name">{b['nu']}</td>
              <td style="color:#C0CEC9">{b['concepto']}</td>
              <td>{b['periodo']}</td>
              <td>{b['fecha']}</td>
              <td class="kc-val">${b['monto']:,.2f}</td>
            </tr>""" for b in bonos)
            st.markdown(f"""<table class="kc-tbl">
              <thead><tr><th>ID</th><th>Usuario</th><th>Concepto</th><th>Periodo</th><th>Fecha</th><th>Monto</th></tr></thead>
              <tbody>{rows}</tbody>
            </table>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("🗑️  Eliminar bono"):
                bopts = {f"#{b['id']} — {b['nu']} · {b['concepto']} · ${b['monto']:,.2f}": b["id"] for b in bonos}
                sb    = st.selectbox("Seleccionar bono", list(bopts.keys()), key="db")
                if st.button("Eliminar bono seleccionado", type="primary"):
                    conn = get_db()
                    conn.execute("DELETE FROM bonos WHERE id=?", (bopts[sb],))
                    conn.commit(); conn.close()
                    st.session_state.msg = ("Bono eliminado.", "s")
                    st.rerun()
        else:
            st.markdown('<div class="kc-empty"><span class="ico">💰</span><p>No hay bonos registrados aun.</p></div>',
                        unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
if not st.session_state.logged_in:
    view_login()
elif st.session_state.rol == "admin":
    view_admin()
else:
    view_usuario()
