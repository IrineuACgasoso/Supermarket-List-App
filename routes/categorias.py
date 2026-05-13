from flask import Blueprint, request, redirect, url_for
from flask_login import login_required

from database import conectar

categorias_bp = Blueprint("categorias", __name__)


@categorias_bp.route("/nova_categoria", methods=["POST"])
@login_required
def nova_categoria():
    nome        = request.form.get("nome_categoria", "").strip()
    produto_ids = request.form.getlist("produtos_categoria")

    if not nome:
        return redirect(url_for("main.index"))

    cx = conectar()
    if cx.execute(
        "SELECT 1 FROM categorias WHERE LOWER(nome) = LOWER(?)", (nome,)
    ).fetchone():
        cx.close()
        return redirect(url_for("main.index"))

    cx.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
    cx.commit()
    cat_id = cx.execute("SELECT last_insert_rowid()").fetchone()[0]
    _associar_produtos(cx, cat_id, produto_ids)
    cx.close()
    return redirect(url_for("main.index"))


@categorias_bp.route("/editar_categoria/<int:cat_id>", methods=["POST"])
@login_required
def editar_categoria(cat_id):
    novo_nome   = request.form.get("novo_nome_categoria", "").strip()
    produto_ids = request.form.getlist("produtos_categoria")

    if not novo_nome:
        return redirect(url_for("main.index"))

    cx = conectar()
    if cx.execute(
        "SELECT 1 FROM categorias WHERE LOWER(nome) = LOWER(?) AND id != ?",
        (novo_nome, cat_id),
    ).fetchone():
        cx.close()
        return redirect(url_for("main.index"))

    cx.execute("UPDATE categorias SET nome = ? WHERE id = ?", (novo_nome, cat_id))
    cx.execute("DELETE FROM produto_categoria WHERE categoria_id = ?", (cat_id,))
    _associar_produtos(cx, cat_id, produto_ids)
    cx.close()
    return redirect(url_for("main.index"))


@categorias_bp.route("/remover_categoria/<int:cat_id>")
@login_required
def remover_categoria(cat_id):
    cx = conectar()
    cx.execute("DELETE FROM produto_categoria WHERE categoria_id = ?", (cat_id,))
    cx.execute("DELETE FROM categorias WHERE id = ?", (cat_id,))
    cx.commit()
    cx.close()
    return redirect(url_for("main.index"))


# ── Helper interno ────────────────────────────────────────────────────────────

def _associar_produtos(cx, cat_id: int, produto_ids: list):
    for pid in produto_ids:
        try:
            cx.execute(
                "INSERT INTO produto_categoria (produto_id, categoria_id) VALUES (?, ?)",
                (int(pid), cat_id),
            )
        except Exception:
            pass
    cx.commit()