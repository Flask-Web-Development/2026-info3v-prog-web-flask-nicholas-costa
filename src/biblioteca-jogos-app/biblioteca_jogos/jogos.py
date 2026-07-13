from flask import Blueprint, render_template

bp = Blueprint("jogos", __name__)

@bp.route("/")
def index():
    return render_template("jogos/index.html")