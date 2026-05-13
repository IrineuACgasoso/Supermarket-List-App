"""
backup_banco.py — Roda como tarefa agendada no PythonAnywhere
Faz commit do banco.db direto pro GitHub toda vez que for executado.

Como configurar no PythonAnywhere:
  1. Vá em Tasks → Add a new scheduled task
  2. Coloque o comando:  python3 /home/amarantesuplist/Lista-Supermercado/backup_banco.py
  3. Escolha a frequência (ex: diariamente)

Pré-requisito: seu repositório no GitHub deve aceitar push sem senha.
Para isso, use um Personal Access Token (PAT):
  - GitHub → Settings → Developer settings → Personal access tokens → Generate new token
  - No terminal Bash do PythonAnywhere, rode uma vez:
      git remote set-url origin https://SEU_TOKEN@github.com/usuario/repo.git
"""


import os
import subprocess
from datetime import datetime

# Pasta do projeto (ajuste se necessário)
PROJETO = os.path.expanduser('~/Lista-Supermercado')

def rodar(cmd):
    resultado = subprocess.run(cmd, cwd=PROJETO, capture_output=True, text=True)
    if resultado.returncode != 0:
        print(f"ERRO: {cmd}\n{resultado.stderr}")
    else:
        print(f"OK: {' '.join(cmd)}")
    return resultado.returncode == 0

agora = datetime.now().strftime('%Y-%m-%d %H:%M')
print(f"\n=== Backup iniciado: {agora} ===")

rodar(['git', 'add', 'banco.db'])
rodar(['git', 'commit', '-m', f'backup automático: {agora}'])
rodar(['git', 'push'])

print("=== Backup concluído ===\n")