import os
import uuid

from PIL import Image
from werkzeug.utils import secure_filename

from config import Config


def _extensao_permitida(nome_arquivo: str) -> bool:
    return (
        "." in nome_arquivo
        and nome_arquivo.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    )


def _mime_valido(file_storage) -> bool:
    """
    Abre o arquivo com Pillow para confirmar que é uma imagem real.
    Protege contra arquivos renomeados (ex: malware.exe → foto.jpg).
    """
    try:
        file_storage.stream.seek(0)
        img = Image.open(file_storage.stream)
        img.verify()          # lança exceção se corrompido ou falso
        file_storage.stream.seek(0)
        return True
    except Exception:
        return False


def salvar_imagem(file_storage, nome_base: str) -> str | None:
    """
    Valida e salva um upload de imagem.

    Retorna o nome do arquivo salvo, ou None se inválido.

    Parâmetros:
        file_storage — objeto FileStorage do Flask (request.files['...'])
        nome_base    — string usada como prefixo do nome gerado (ex: nome do produto)
    """
    if not file_storage or not file_storage.filename:
        return None

    if not _extensao_permitida(file_storage.filename):
        return None

    if not _mime_valido(file_storage):
        return None

    ext = file_storage.filename.rsplit(".", 1)[1].lower()
    nome_arquivo = f"{secure_filename(nome_base.lower())}_{uuid.uuid4().hex[:8]}.{ext}"
    destino = os.path.join(Config.UPLOAD_FOLDER, nome_arquivo)
    file_storage.save(destino)
    return nome_arquivo