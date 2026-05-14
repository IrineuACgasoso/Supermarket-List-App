import os
import shutil

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

PASTA_STATIC = os.path.join(BASE_DIR, "static")
PASTA_UPLOADS = "/home/seuusuario/supermarket_data/uploads"

os.makedirs(PASTA_UPLOADS, exist_ok=True)

extensoes_validas = (
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif"
)

movidos = 0

for raiz, dirs, arquivos in os.walk(PASTA_STATIC):

    for arquivo in arquivos:

        if arquivo.lower().endswith(extensoes_validas):

            origem = os.path.join(raiz, arquivo)
            destino = os.path.join(PASTA_UPLOADS, arquivo)

            if not os.path.exists(destino):

                shutil.move(origem, destino)

                print(f"Movido: {arquivo}")
                movidos += 1

print(f"\nTotal movidos: {movidos}")