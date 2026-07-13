from flask import Blueprint, render_template, request, redirect

bp = Blueprint("auth", __name__, url_prefix="/auth")

usuarios = []


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        usuario = {
            "username": request.form["username"],
            "password": request.form["password"]
        }

        usuarios.append(usuario)

        return redirect("/auth/login")

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        return redirect("/")

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    return redirect("/")