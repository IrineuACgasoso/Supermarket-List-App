from flask import Flask, url_for

from config import Config
from extensions import limiter, login_manager
from database import inicializar

import models  # registra o user_loader no login_manager

from routes.auth       import auth_bp
from routes.main       import main_bp
from routes.produtos   import produtos_bp
from routes.categorias import categorias_bp

def url_imagem(nome_arquivo):
    if not nome_arquivo:
        return ""

    return url_for(
        "produtos.upload_file",
        filename=nome_arquivo
    )

def create_app():
    app = Flask(__name__)
    app.jinja_env.globals["url_imagem"] = url_imagem
    app.config.from_object(Config)

    import os

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Extensões
    limiter.init_app(app)
    login_manager.init_app(app)

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(categorias_bp)

    return app


app = create_app()
inicializar()

if __name__ == "__main__":
    app.run()