import tkinter as tk
from tkinter import messagebox, Text, Scrollbar, Listbox, Entry
from ttkbootstrap import Style
from ttkbootstrap.widgets import Frame, Label, Button, Combobox, Notebook
import json
import time
import requests

from core.colecoes import salvar_colecao, carregar_colecao
from core.util import salvar_resposta_em_arquivo

def iniciar_interface():
    style = Style("superhero")
    janela = style.master
    janela.title("🧪 PyAPI Tester")
    janela.geometry("1000x800")

    frame = Frame(janela, padding=10)
    frame.pack(fill="both", expand=True)

    # URL e Método
    Label(frame, text="URL da API:").pack(anchor="w")
    global entry_url
    entry_url = Entry(frame, width=100)
    entry_url.pack(pady=5)

    Label(frame, text="Método HTTP:").pack(anchor="w")
    global metodo_var
    metodo_var = tk.StringVar(value="GET")
    combo_metodo = Combobox(frame, textvariable=metodo_var, values=["GET", "POST", "PUT", "DELETE", "PATCH"])
    combo_metodo.pack(pady=5)

    # Token JWT
    Label(frame, text="Token JWT (opcional):").pack(anchor="w")
    global entry_token
    entry_token = Entry(frame, width=100)
    entry_token.pack(pady=2)
    Button(frame, text="🗭️ Adicionar ao Header", bootstyle="warning", command=adicionar_token_ao_header).pack(pady=5)

    # Headers e Body
    Label(frame, text="Headers (JSON):").pack(anchor="w")
    global text_headers
    text_headers = Text(frame, height=5)
    text_headers.pack(fill="x", pady=5)

    Label(frame, text="Body (JSON):").pack(anchor="w")
    global text_body
    text_body = Text(frame, height=5)
    text_body.pack(fill="x", pady=5)

    # Nome da coleção e botões
    Label(frame, text="Nome da Coleção:").pack(anchor="w")
    global entry_nome_colecao
    entry_nome_colecao = Entry(frame, width=50)
    entry_nome_colecao.pack(pady=2)
    Button(frame, text="📏 Salvar como Colecao", bootstyle="secondary", command=salvar_como_colecao).pack(pady=2)
    Button(frame, text="📂 Carregar Colecao", bootstyle="primary", command=carregar_colecao_por_nome).pack(pady=2)

    Button(frame, text="🚀 Enviar Requisição", bootstyle="success", command=enviar_requisicao).pack(pady=10)

    global label_status, label_tempo
    label_status = Label(frame, text="Status: ---")
    label_status.pack()
    label_tempo = Label(frame, text="Tempo: ---")
    label_tempo.pack()

    # Abas de resposta
    global text_body_response, text_headers_response
    Label(frame, text="Resposta:").pack(anchor="w")
    notebook = Notebook(frame)
    notebook.pack(fill="both", expand=True)

    frame_body = Frame(notebook)
    text_body_response = Text(frame_body, height=15)
    text_body_response.pack(fill="both", expand=True)
    notebook.add(frame_body, text="Body")

    frame_headers = Frame(notebook)
    text_headers_response = Text(frame_headers, height=15)
    text_headers_response.pack(fill="both", expand=True)
    notebook.add(frame_headers, text="Headers")

    Button(frame, text="📄 Copiar Resposta", bootstyle="info", command=copiar_resposta).pack(pady=5)

    # Botões para exportar resposta
    btn_frame = Frame(frame)
    btn_frame.pack(pady=5)
    Button(btn_frame, text="📂 Salvar como .json", bootstyle="secondary", command=salvar_resposta_json).pack(side="left", padx=5)
    Button(btn_frame, text="📜 Salvar como .txt", bootstyle="secondary", command=salvar_resposta_txt).pack(side="left", padx=5)

    # Testes em lote
    Label(frame, text="🖁️ Testes em Lote (1 URL por linha):").pack(anchor="w")
    global text_lote_urls
    text_lote_urls = Text(frame, height=5)
    text_lote_urls.pack(fill="x", pady=5)

    Label(frame, text="Método para o lote:").pack(anchor="w")
    global lote_metodo_var
    lote_metodo_var = tk.StringVar(value="GET")
    combo_lote_metodo = Combobox(frame, textvariable=lote_metodo_var, values=["GET", "POST", "PUT", "DELETE", "PATCH"])
    combo_lote_metodo.pack(pady=5)

    Button(frame, text="🚀 Executar Lote", bootstyle="danger", command=executar_lote).pack(pady=5)

    Label(frame, text="Resultado dos Testes em Lote:").pack(anchor="w")
    global text_lote_resultado
    text_lote_resultado = Text(frame, height=10)
    text_lote_resultado.pack(fill="both", expand=True, pady=5)

    janela.mainloop()

# ==== Funções Auxiliares ====

def enviar_requisicao():
    url = entry_url.get()
    metodo = metodo_var.get()
    headers_text = text_headers.get("1.0", tk.END).strip()
    body_text = text_body.get("1.0", tk.END).strip()

    try:
        headers = json.loads(headers_text) if headers_text else {}
    except json.JSONDecodeError:
        messagebox.showerror("Erro", "Headers não estão em JSON válido.")
        return

    try:
        body = json.loads(body_text) if body_text else None
    except json.JSONDecodeError:
        messagebox.showerror("Erro", "Body não está em JSON válido.")
        return

    try:
        inicio = time.time()
        resposta = requests.request(metodo, url, headers=headers, json=body)
        fim = time.time()

        label_status.config(text=f"Status: {resposta.status_code}")
        label_tempo.config(text=f"Tempo: {fim - inicio:.2f}s")

        try:
            resposta_json = resposta.json()
            texto_body = json.dumps(resposta_json, indent=2, ensure_ascii=False)
        except ValueError:
            texto_body = resposta.text

        text_body_response.delete("1.0", tk.END)
        text_body_response.insert(tk.END, texto_body)

        headers_formatados = json.dumps(dict(resposta.headers), indent=2)
        text_headers_response.delete("1.0", tk.END)
        text_headers_response.insert(tk.END, headers_formatados)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro ao enviar requisição:\n{e}")

def copiar_resposta():
    aba_atual = text_body_response.get("1.0", tk.END).strip()
    if not aba_atual:
        messagebox.showwarning("Vazio", "Nenhuma resposta para copiar.")
        return
    janela = tk.Tk()
    janela.withdraw()
    janela.clipboard_clear()
    janela.clipboard_append(aba_atual)
    janela.update()
    janela.destroy()
    messagebox.showinfo("Copiado", "Resposta copiada com sucesso!")

def salvar_como_colecao():
    nome = entry_nome_colecao.get()
    if not nome:
        messagebox.showwarning("Nome vazio", "Digite um nome para a coleção.")
        return

    dados = {
        "url": entry_url.get(),
        "metodo": metodo_var.get(),
        "headers": text_headers.get("1.0", tk.END).strip(),
        "body": text_body.get("1.0", tk.END).strip()
    }

    try:
        salvar_colecao(nome, dados)
        messagebox.showinfo("Salvo", f"Coleção '{nome}' salva com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro ao salvar", str(e))

def carregar_colecao_por_nome():
    nome = entry_nome_colecao.get()
    if not nome:
        messagebox.showwarning("Nome vazio", "Digite o nome da coleção.")
        return

    try:
        dados = carregar_colecao(nome)
        entry_url.delete(0, tk.END)
        entry_url.insert(0, dados["url"])
        metodo_var.set(dados["metodo"])
        text_headers.delete("1.0", tk.END)
        text_headers.insert(tk.END, dados["headers"])
        text_body.delete("1.0", tk.END)
        text_body.insert(tk.END, dados["body"])
        messagebox.showinfo("Carregado", f"Coleção '{nome}' carregada com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro ao carregar", str(e))

def salvar_resposta_json():
    conteudo = text_body_response.get("1.0", tk.END).strip()
    if not conteudo:
        messagebox.showwarning("Sem conteúdo", "Nenhuma resposta para salvar.")
        return
    caminho = salvar_resposta_em_arquivo(conteudo, tipo="json")
    messagebox.showinfo("Salvo", f"Resposta salva em:\n{caminho}")

def salvar_resposta_txt():
    conteudo = text_body_response.get("1.0", tk.END).strip()
    if not conteudo:
        messagebox.showwarning("Sem conteúdo", "Nenhuma resposta para salvar.")
        return
    caminho = salvar_resposta_em_arquivo(conteudo, tipo="txt")
    messagebox.showinfo("Salvo", f"Resposta salva em:\n{caminho}")

def adicionar_token_ao_header():
    token = entry_token.get().strip()
    if not token:
        messagebox.showwarning("Token vazio", "Digite um token JWT.")
        return

    try:
        headers_atual = text_headers.get("1.0", tk.END).strip()
        headers_json = json.loads(headers_atual) if headers_atual else {}
        headers_json["Authorization"] = f"Bearer {token}"
        text_headers.delete("1.0", tk.END)
        text_headers.insert(tk.END, json.dumps(headers_json, indent=2))
        messagebox.showinfo("Token adicionado", "Token JWT adicionado ao header com sucesso.")
    except json.JSONDecodeError:
        messagebox.showerror("Erro", "Headers não estão em JSON válido.")

def executar_lote():
    urls = text_lote_urls.get("1.0", tk.END).strip().splitlines()
    metodo = lote_metodo_var.get()
    headers_text = text_headers.get("1.0", tk.END).strip()
    body_text = text_body.get("1.0", tk.END).strip()

    try:
        headers = json.loads(headers_text) if headers_text else {}
    except json.JSONDecodeError:
        messagebox.showerror("Erro", "Headers inválidos.")
        return

    try:
        body = json.loads(body_text) if body_text else None
    except json.JSONDecodeError:
        messagebox.showerror("Erro", "Body inválido.")
        return

    if not urls:
        messagebox.showwarning("URLs vazias", "Digite pelo menos uma URL.")
        return

    text_lote_resultado.delete("1.0", tk.END)

    for url in urls:
        url = url.strip()
        if not url:
            continue
        try:
            inicio = time.time()
            resposta = requests.request(metodo, url, headers=headers, json=body)
            fim = time.time()
            resultado = f"[{metodo}] {url}\n→ Status: {resposta.status_code}, Tempo: {fim - inicio:.2f}s\n\n"
        except Exception as e:
            resultado = f"[{metodo}] {url}\n→ Erro: {str(e)}\n\n"
        text_lote_resultado.insert(tk.END, resultado)
