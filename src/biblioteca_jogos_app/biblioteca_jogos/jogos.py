from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from .auth import login_required
from .db import get_db


bp = Blueprint("jogos", __name__)


@bp.route("/")
def index():
    db = get_db()

    jogos = db.execute(
        """
        SELECT j.id, nome, plataforma, genero, status, usuario_id, username
        FROM jogo j JOIN usuario u ON j.usuario_id = u.id
        ORDER BY j.id DESC
        """
    ).fetchall()

    return render_template("jogos/index.html", jogos=jogos)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        nome = request.form["nome"]
        plataforma = request.form["plataforma"]
        genero = request.form["genero"]
        status = request.form["status"]

        db = get_db()

        db.execute(
            """
            INSERT INTO jogo
            (nome, plataforma, genero, status, usuario_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nome, plataforma, genero, status, g.usuario["id"])
        )

        db.commit()

        return redirect(url_for("jogos.index"))

    return render_template("jogos/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    db = get_db()

    jogo = db.execute(
        "SELECT * FROM jogo WHERE id = ?",
        (id,)
    ).fetchone()

    if jogo is None:
        return redirect(url_for("jogos.index"))

    if request.method == "POST":
        nome = request.form["nome"]
        plataforma = request.form["plataforma"]
        genero = request.form["genero"]
        status = request.form["status"]

        db.execute(
            """
            UPDATE jogo
            SET nome = ?, plataforma = ?, genero = ?, status = ?
            WHERE id = ?
            """,
            (nome, plataforma, genero, status, id)
        )

        db.commit()

        return redirect(url_for("jogos.index"))

    return render_template("jogos/update.html", jogo=jogo)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    db = get_db()

    db.execute(
        "DELETE FROM jogo WHERE id = ?",
        (id,)
    )

    db.commit()

    return redirect(url_for("jogos.index"))