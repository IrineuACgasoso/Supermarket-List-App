import sqlite3
from config import Config


def conectar():
    cx = sqlite3.connect(Config.DATABASE_PATH)
    cx.row_factory = sqlite3.Row
    return cx


def inicializar():
    cx = conectar()

    cx.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            username   TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            is_admin   INTEGER DEFAULT 0
        )
    """)
    cx.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            nome   TEXT NOT NULL,
            imagem TEXT NOT NULL
        )
    """)
    cx.execute("""
        CREATE TABLE IF NOT EXISTS lista_compras (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            nome       TEXT NOT NULL,
            quantidade INTEGER NOT NULL
        )
    """)
    cx.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
    """)
    cx.execute("""
        CREATE TABLE IF NOT EXISTS produto_categoria (
            produto_id   INTEGER NOT NULL,
            categoria_id INTEGER NOT NULL,
            PRIMARY KEY (produto_id, categoria_id),
            FOREIGN KEY (produto_id)   REFERENCES produtos(id),
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    """)

    # Produtos de exemplo apenas no primeiro uso
    if cx.execute("SELECT COUNT(*) FROM produtos").fetchone()[0] == 0:
        cx.executemany(
            "INSERT INTO produtos (nome, imagem) VALUES (?, ?)",
            [("Arroz", "arroz.jpg"), ("Feijão", "feijao.jpg"), ("Leite", "leite.jpg")],
        )
        cx.commit()

    cx.close()


def lista_json(cx):
    """Retorna a lista de compras como lista de dicts (para jsonify)."""
    rows = cx.execute(
        "SELECT * FROM lista_compras ORDER BY nome ASC"
    ).fetchall()
    return [{"nome": r["nome"], "quantidade": r["quantidade"]} for r in rows]