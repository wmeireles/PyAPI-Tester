import os
from datetime import datetime

RESPOSTAS_DIR = "respostas"

def garantir_diretorio_respostas():
    if not os.path.exists(RESPOSTAS_DIR):
        os.makedirs(RESPOSTAS_DIR)

def gerar_nome_arquivo(ext):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"resposta_{timestamp}.{ext}"

def salvar_resposta_em_arquivo(conteudo, tipo="json"):
    garantir_diretorio_respostas()
    nome_arquivo = gerar_nome_arquivo(tipo)
    caminho = os.path.join(RESPOSTAS_DIR, nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return caminho
