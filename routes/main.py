from flask import Blueprint, render_template
from flask_login import login_required

from database import conectar

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def index():
    cx         = conectar()
    produtos   = cx.execute("SELECT * FROM produtos ORDER BY nome ASC").fetchall()
    lista      = cx.execute("SELECT * FROM lista_compras ORDER BY nome ASC").fetchall()
    categorias = cx.execute("SELECT * FROM categorias ORDER BY nome ASC").fetchall()

    produto_cats = {}
    for row in cx.execute("SELECT produto_id, categoria_id FROM produto_categoria").fetchall():
        produto_cats.setdefault(row["produto_id"], []).append(row["categoria_id"])

    cx.close()
    return render_template(
        "index.html",
        produtos=produtos,
        lista=lista,
        categorias=categorias,
        produto_cats=produto_cats,
    )