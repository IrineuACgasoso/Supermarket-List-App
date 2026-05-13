from flask import Blueprint, request, redirect, url_for, jsonify, send_from_directory
from flask_login import login_required

from config import Config
from database import conectar, lista_json
from extensions import limiter
from utils.uploads import salvar_imagem

produtos_bp = Blueprint("produtos", __name__)


# ── API AJAX ──────────────────────────────────────────────────────────────────

@produtos_bp.route("/api/adicionar", methods=["POST"])
@login_required
def api_adicionar():
    produto    = request.form.get("produto", "").strip()
    quantidade = int(request.form.get("quantidade", 1))

    cx        = conectar()
    existente = cx.execute(
        "SELECT * FROM lista_compras WHERE nome = ?", (produto,)
    ).fetchone()

    if existente:
        cx.execute(
            "UPDATE lista_compras SET quantidade = ? WHERE nome = ?",
            (existente["quantidade"] + quantidade, produto),
        )
    else:
        cx.execute(
            "INSERT INTO lista_compras (nome, quantidade) VALUES (?, ?)",
            (produto, quantidade),
        )

    cx.commit()
    resultado = lista_json(cx)
    cx.close()
    return jsonify(resultado)


@produtos_bp.route("/api/remover/<nome_do_produto>")
@login_required
def api_remover(nome_do_produto):
    cx = conectar()
    cx.execute("DELETE FROM lista_compras WHERE nome = ?", (nome_do_produto,))
    cx.commit()
    resultado = lista_json(cx)
    cx.close()
    return jsonify(resultado)


# ── Catálogo AJAX ──────────────────────────────────────────────────────────────────

@produtos_bp.route("/novo_produto", methods=["POST"])
@login_required
@limiter.limit("10 per minute")
def novo_produto():
    nome   = request.form.get("nome_produto", "").strip()
    imagem = request.files.get("imagem_produto")

    if not nome:
        return jsonify({"erro": "O nome do produto é obrigatório"}), 400
    
    cx     = conectar()
    # Verifica se o produto já existe para evitar duplicatas
    if cx.execute("SELECT 1 FROM produtos WHERE LOWER(nome) = LOWER(?)", (nome,)).fetchone():
        cx.close()
        return jsonify({"erro": "Este produto já existe no catálogo"}), 400
    # Salva a imagem (ou usa a padrão se não for enviada)
    nome_arquivo = salvar_imagem(imagem, nome) or "default.jpg"

    cursor = cx.execute(
        "INSERT INTO produtos (nome, imagem) VALUES (?, ?)",
        (nome, nome_arquivo)
    )
    novo_id = cursor.lastrowid
    cx.commit()
    cx.close()

    return jsonify({
        "id": novo_id,
        "nome": nome,
        "imagem": url_for('static', filename=nome_arquivo)
    })


@produtos_bp.route("/editar_produto/<int:produto_id>", methods=["POST"])
@login_required
@limiter.limit("10 per minute")
def editar_produto(produto_id):
    novo_nome = request.form.get("novo_nome", "").strip()
    imagem    = request.files.get("imagem_produto")

    # Validação básica
    if not novo_nome:
        return jsonify({"erro": "O nome não pode estar vazio"}), 400
    
    cx      = conectar()
    produto = cx.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,)).fetchone()

    if not produto:
        cx.close()
        return jsonify({"erro": "Produto não encontrado"}), 404
    
    # Verifica se já existe outro produto com o mesmo nome (exceto ele mesmo)
    if cx.execute(
        "SELECT 1 FROM produtos WHERE LOWER(nome) = LOWER(?) AND id != ?",
        (novo_nome, produto_id),
    ).fetchone():
        cx.close()
        return jsonify({"erro": "Já existe um produto com este nome"}), 400

    # Usa a imagem nova se válida, senão mantém a atual
    nome_arquivo = salvar_imagem(imagem, novo_nome) or produto["imagem"]

    cx.execute(
        "UPDATE produtos SET nome = ?, imagem = ? WHERE id = ?",
        (novo_nome, nome_arquivo, produto_id),
    )
    cx.commit()
    cx.close()

    # RETORNO PARA O AJAX: Envia os dados atualizados para o JS
    return jsonify({
        "id": produto_id,
        "nome": novo_nome,
        "imagem": url_for('static', filename=nome_arquivo)
    })


@produtos_bp.route("/remover_catalogo/<nome_do_produto>")
@login_required
def remover_catalogo(nome_do_produto):
    cx      = conectar()
    produto = cx.execute(
        "SELECT id FROM produtos WHERE nome = ?", (nome_do_produto,)
    ).fetchone()

    if produto:
        cx.execute("DELETE FROM produto_categoria WHERE produto_id = ?", (produto["id"],))
        cx.execute("DELETE FROM produtos WHERE id = ?", (produto["id"],))
        cx.commit()

    cx.close()
    return redirect(url_for("main.index"))


# ── Service Worker (precisa servir da raiz) ───────────────────────────────────

@produtos_bp.route("/sw.js")
def serve_sw():
    return send_from_directory("static", "sw.js")