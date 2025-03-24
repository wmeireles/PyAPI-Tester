# PyAPI Tester

**PyAPI Tester** é uma ferramenta desktop escrita em Python para realizar testes de APIs REST de forma simples, intuitiva e com interface moderna.
Ideal para desenvolvedores, testadores e profissionais de T.I que precisam enviar requisições HTTP com facilidade.

![Banner ou captura de tela aqui]

---

## 🚀 Funcionalidades

- [x] Enviar requisições HTTP (GET, POST, PUT, DELETE, PATCH)
- [x] Inserir headers e corpo da requisição (em JSON)
- [x] Visualização da resposta com abas para Body e Headers
- [x] Copiar e exportar resposta como `.json` ou `.txt`
- [x] Salvar e carregar coleções de requisições em arquivos `.json`
- [x] Campo para Token JWT com adição automática ao header
- [x] Testes em lote com múltiplas URLs
- [x] Interface moderna com `ttkbootstrap`

---

## 🧱 Tech Stack

- Python 3.10+
- `requests`
- `ttkbootstrap`
- `tkinter` (nativo)

---

## 📁 Estrutura de Pastas

```bash
pyapi-tester/
├── main.py                   # Inicializa a aplicação
├── core/
│   ├── colecoes.py           # Salvar/carregar coleções
│   ├── requisicoes.py        # (em breve)
│   └── util.py               # Funções auxiliares (exportação, pasta, nome de arquivo)
├── ui/
│   ├── layout.py             # Interface principal
│   ├── componentes.py        # (em breve)
│   └── temas.py              # (em breve - alternador de tema)
├── colecoes/                 # Armazena coleções salvas em JSON
├── respostas/                # Exportações de resposta
└── README.md
```

---

## ⚖️ Como usar

1. Clone o repositório:
```bash
git clone https://github.com/seuusuario/pyapi-tester.git
cd pyapi-tester
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o projeto:
```bash
python main.py
```

---

## ✍️ To-Do / Melhorias Futuras

- [ ] Alternador de tema (light/dark)
- [ ] Abas para autenticação básica, Bearer, etc
- [ ] Editor JSON com destaque de sintaxe
- [ ] Gráfico de tempo de resposta por endpoint (com matplotlib ou plotly)
- [ ] Suporte a arquivos `.env` para variáveis de ambiente

---

## 🚀 Autor

Desenvolvido por **Willian Meireles**  
[LinkedIn](https://linkedin.com/in/willianmeireles) | [GitHub](https://github.com/wmeireles)

---

> Este projeto está em evolução constante ✨
> Contribuições e ideias são muito bem-vindas!

