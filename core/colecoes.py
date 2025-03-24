import os
import json

COLECOES_DIR = "colecoes"

def garantir_diretorio():
    if not os.path.exists(COLECOES_DIR):
        os.makedirs(COLECOES_DIR)

def salvar_colecao(nome_arquivo, dados):
    garantir_diretorio()
    caminho = os.path.join(COLECOES_DIR, f"{nome_arquivo}.json")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def carregar_colecao(nome_arquivo):
    caminho = os.path.join(COLECOES_DIR, f"{nome_arquivo}.json")
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Coleção '{nome_arquivo}' não encontrada.")
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)
