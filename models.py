from flask_login import UserMixin
from database import conectar
from extensions import login_manager


class Usuario(UserMixin):
    def __init__(self, id, username, senha_hash, is_admin):
        self.id         = id
        self.username   = username
        self.senha_hash = senha_hash
        self.is_admin   = is_admin


@login_manager.user_loader
def load_user(user_id):
    cx   = conectar()
    user = cx.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    cx.close()
    if user:
        return Usuario(user["id"], user["username"], user["senha_hash"], user["is_admin"])
    return None