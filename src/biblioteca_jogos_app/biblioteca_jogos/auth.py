import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()

        error = None

        if not username:
            error = "Usuário é obrigatório."

        elif not password:
            error = "Senha é obrigatória."

        elif db.execute(
            "SELECT id FROM usuario WHERE username = ?",
            (username,)
        ).fetchone() is not None:
            error = f"O usuário {username} já existe."

        if error is None:
            db.execute(
                "INSERT INTO usuario (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password))
            )

            db.commit()

            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()

        usuario = db.execute(
            "SELECT * FROM usuario WHERE username = ?",
            (username,)
        ).fetchone()

        error = None

        if usuario is None:
            error = "Usuário incorreto."

        elif not check_password_hash(usuario["password"], password):
            error = "Senha incorreta."

        if error is None:
            session.clear()
            session["usuario_id"] = usuario["id"]

            return redirect(url_for("jogos.index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    usuario_id = session.get("usuario_id")

    if usuario_id is None:
        g.usuario = None

    else:
        g.usuario = get_db().execute(
            "SELECT * FROM usuario WHERE id = ?",
            (usuario_id,)
        ).fetchone()


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("jogos.index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.usuario is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view