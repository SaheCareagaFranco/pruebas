from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "intranet_bonos_secret_key_2024"

DB_PATH = os.path.join(os.path.dirname(__file__), "bonos.db")


# ---------------------------------------------------------------------------
# Base de datos
# ---------------------------------------------------------------------------

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
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id  INTEGER NOT NULL,
            concepto    TEXT    NOT NULL,
            monto       REAL    NOT NULL,
            periodo     TEXT    NOT NULL,
            fecha       TEXT    NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)
    # Admin por defecto
    c.execute("SELECT id FROM usuarios WHERE username = 'admin'")
    if not c.fetchone():
        c.execute(
            "INSERT INTO usuarios (username, password, nombre, rol) VALUES (?, ?, ?, ?)",
            ("admin", "admin123", "Administrador", "admin"),
        )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def usuario_actual():
    return session.get("usuario")


def requiere_login(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not usuario_actual():
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper


def requiere_admin(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not usuario_actual():
            return redirect(url_for("login"))
        if session.get("rol") != "admin":
            flash("Acceso restringido.", "danger")
            return redirect(url_for("dashboard"))
        return fn(*args, **kwargs)
    return wrapper


# ---------------------------------------------------------------------------
# Rutas de autenticación
# ---------------------------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def login():
    if usuario_actual():
        if session.get("rol") == "admin":
            return redirect(url_for("admin_panel"))
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM usuarios WHERE username = ? AND password = ?",
            (username, password),
        ).fetchone()
        conn.close()
        if user:
            session["usuario"] = user["username"]
            session["nombre"] = user["nombre"]
            session["rol"] = user["rol"]
            session["user_id"] = user["id"]
            if user["rol"] == "admin":
                return redirect(url_for("admin_panel"))
            return redirect(url_for("dashboard"))
        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------------------------------------------------------
# Ruta de usuario
# ---------------------------------------------------------------------------

@app.route("/dashboard")
@requiere_login
def dashboard():
    conn = get_db()
    bonos = conn.execute(
        "SELECT * FROM bonos WHERE usuario_id = ? ORDER BY fecha DESC",
        (session["user_id"],),
    ).fetchall()
    conn.close()
    return render_template("user_dashboard.html", bonos=bonos)


# ---------------------------------------------------------------------------
# Rutas de administrador
# ---------------------------------------------------------------------------

@app.route("/admin")
@requiere_admin
def admin_panel():
    conn = get_db()
    usuarios = conn.execute("SELECT * FROM usuarios WHERE rol = 'usuario' ORDER BY nombre").fetchall()
    bonos = conn.execute("""
        SELECT b.*, u.nombre as nombre_usuario, u.username
        FROM bonos b
        JOIN usuarios u ON b.usuario_id = u.id
        ORDER BY b.fecha DESC
    """).fetchall()
    conn.close()
    return render_template("admin_dashboard.html", usuarios=usuarios, bonos=bonos)


@app.route("/admin/agregar_usuario", methods=["POST"])
@requiere_admin
def agregar_usuario():
    nombre   = request.form["nombre"].strip()
    username = request.form["username"].strip()
    password = request.form["password"].strip()

    if not nombre or not username or not password:
        flash("Todos los campos son obligatorios.", "danger")
        return redirect(url_for("admin_panel"))

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO usuarios (username, password, nombre, rol) VALUES (?, ?, ?, 'usuario')",
            (username, password, nombre),
        )
        conn.commit()
        flash(f"Usuario '{nombre}' creado exitosamente.", "success")
    except sqlite3.IntegrityError:
        flash(f"El username '{username}' ya existe.", "danger")
    finally:
        conn.close()
    return redirect(url_for("admin_panel"))


@app.route("/admin/editar_usuario/<int:user_id>", methods=["POST"])
@requiere_admin
def editar_usuario(user_id):
    nombre   = request.form["nombre"].strip()
    password = request.form["password"].strip()

    conn = get_db()
    conn.execute(
        "UPDATE usuarios SET nombre = ?, password = ? WHERE id = ?",
        (nombre, password, user_id),
    )
    conn.commit()
    conn.close()
    flash("Usuario actualizado.", "success")
    return redirect(url_for("admin_panel"))


@app.route("/admin/eliminar_usuario/<int:user_id>", methods=["POST"])
@requiere_admin
def eliminar_usuario(user_id):
    conn = get_db()
    conn.execute("DELETE FROM bonos WHERE usuario_id = ?", (user_id,))
    conn.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    flash("Usuario eliminado.", "success")
    return redirect(url_for("admin_panel"))


@app.route("/admin/agregar_bono", methods=["POST"])
@requiere_admin
def agregar_bono():
    usuario_id = request.form["usuario_id"]
    concepto   = request.form["concepto"].strip()
    monto      = request.form["monto"].strip()
    periodo    = request.form["periodo"].strip()
    fecha      = request.form["fecha"].strip()

    if not all([usuario_id, concepto, monto, periodo, fecha]):
        flash("Todos los campos del bono son obligatorios.", "danger")
        return redirect(url_for("admin_panel"))

    conn = get_db()
    conn.execute(
        "INSERT INTO bonos (usuario_id, concepto, monto, periodo, fecha) VALUES (?, ?, ?, ?, ?)",
        (usuario_id, concepto, float(monto), periodo, fecha),
    )
    conn.commit()
    conn.close()
    flash("Bono agregado exitosamente.", "success")
    return redirect(url_for("admin_panel"))


@app.route("/admin/eliminar_bono/<int:bono_id>", methods=["POST"])
@requiere_admin
def eliminar_bono(bono_id):
    conn = get_db()
    conn.execute("DELETE FROM bonos WHERE id = ?", (bono_id,))
    conn.commit()
    conn.close()
    flash("Bono eliminado.", "success")
    return redirect(url_for("admin_panel"))


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
