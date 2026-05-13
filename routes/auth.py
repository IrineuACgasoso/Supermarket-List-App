from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from database import conectar
from extensions import limiter

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        senha    = request.form.get("senha", "")

        cx   = conectar()
        user = cx.execute(
            "SELECT * FROM usuarios WHERE username = ?", (username,)
        ).fetchone()
        cx.close()

        if user and check_password_hash(user["senha_hash"], senha):
            from models import Usuario
            login_user(Usuario(user["id"], user["username"], user["senha_hash"], user["is_admin"]))
            return redirect(url_for("main.index"))

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))