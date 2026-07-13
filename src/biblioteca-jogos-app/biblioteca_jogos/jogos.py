from flask import Blueprint, render_template, request, redirect

bp = Blueprint("jogos", __name__)

jogos = []

@bp.route("/")
def index():
    return render_template("jogos/index.html", jogos=jogos)


@bp.route("/criar", methods=("GET", "POST"))
def criar():
    if request.method == "POST":
        jogo = {
            "nome": request.form["nome"],
            "plataforma": request.form["plataforma"],
            "genero": request.form["genero"],
            "status": request.form["status"]
        }

        jogos.append(jogo)

        return redirect("/")

    return render_template("jogos/criar.html")