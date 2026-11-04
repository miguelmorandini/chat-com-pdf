# Chat com PDF — IA Generativa e RAG

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/miguelmorandini/chat-com-pdf/blob/main/chat_com_pdf.ipynb)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-GenAI%20SDK-orange?logo=google)
![Gradio](https://img.shields.io/badge/UI-Gradio-ff7c00?logo=gradio)
![License](https://img.shields.io/badge/License-MIT-green)

Assistente de perguntas e respostas baseado em documentos PDF utilizando a arquitetura RAG (Retrieval-Augmented Generation) com a API do Google Gemini e interface web em Gradio.

O projeto resolve o desafio de mitigar alucinacoes ao responder sobre documentos tecnicos, garantindo respostas embasadas exclusivamente no texto fornecido e citando a numeracao das paginas consultadas.

---

## Objetivo e Requisitos

- **Ambiente:** Executavel no Google Colab e em ambiente local.
- **Extracao:** Mapeamento de texto por pagina com `PyPDF2`.
- **Chunking:** Segmentacao em blocos com overlap para manter a continuidade do contexto.
- **Recuperacao:** Busca por similaridade de cosseno via TF-IDF (`scikit-learn`).
- **Prompt Anti-Alucinacao:** Regras explicitas para evitar invencoes e exigir citacao de paginas.
- **Entregaveis:** 
  - 3 perguntas tecnicas respondidas com citacao de pagina.
  - 1 pergunta fora de escopo respondida com: *"Nao encontrei essa informacao no documento."*

---

## Arquitetura do Pipeline RAG

```
                 +-----------------------------------------+
                 |            Documento PDF                |
                 +-----------------------------------------+
                                      |
                                      v
                 +-----------------------------------------+
                 |    1. Extracao por Pagina (PyPDF2)      |
                 +-----------------------------------------+
                                      |
                                      v
                 +-----------------------------------------+
                 |    2. Chunking com Overlap (800 / 150)  |
                 +-----------------------------------------+
                                      |
                                      v
                 +-----------------------------------------+
                 |   3. Matriz TF-IDF e Indice Vetorial    |
                 +-----------------------------------------+
                                      |
 Pergunta do Usuario  --------------->+ (Similaridade de Cosseno)
                                      |
                                      v
                 +-----------------------------------------+
                 |     Top-k Trechos Relevantes + Paginas  |
                 +-----------------------------------------+
                                      |
                                      v
                 +-----------------------------------------+
                 | 4. Prompt Anti-Alucinacao + Contexto     |
                 +-----------------------------------------+
                                      |
                                      v
                 +-----------------------------------------+
                 |    5. Google Gemini (API GenAI)         |
                 +-----------------------------------------+
                                      |
                                      v
                 +-----------------------------------------+
                 | Resposta com Citacao da Pagina (Gradio) |
                 +-----------------------------------------+
```

---

## Como Executar

### Opcao 1: Google Colab
Abra o notebook diretamente na nuvem:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/miguelmorandini/chat-com-pdf/blob/main/chat_com_pdf.ipynb)

> Configure sua chave do Google AI Studio nos **Secrets** do Colab com o nome `GEMINI_API_KEY`.

---

### Opcao 2: Localmente

1. **Clone o repositorio:**
   ```bash
   git clone https://github.com/miguelmorandini/chat-com-pdf.git
   cd chat-com-pdf
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   ```

3. **Instale as dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Defina a variavel de ambiente:**
   ```bash
   # Windows (PowerShell):
   $env:GEMINI_API_KEY="sua_chave_aqui"

   # Linux/Mac:
   export GEMINI_API_KEY="sua_chave_aqui"
   ```

5. **Execute:**
   ```bash
   jupyter notebook chat_com_pdf.ipynb
   # ou execute o app Gradio diretamente:
   python app.py
   ```

---

## Validacao do Desafio

| Tipo de Teste | Pergunta | Comportamento Esperado |
| :--- | :--- | :--- |
| **Pergunta Tecnica 1** | *What is Delta Lake and how does it bring reliability?* | Resposta precisa citando as paginas (ex: Pag. 3 e 8) |
| **Pergunta Tecnica 2** | *What is a Lakehouse and what problems does it solve?* | Resumo conceitual citando as Pag. 5, 6 e 13 |
| **Pergunta Tecnica 3** | *How does Delta Lake handle ACID transactions?* | Explicacao do log de transacoes citando a Pag. 8 e 13 |
| **Teste Anti-Alucinacao** | *Qual e a escalacao da selecao brasileira em 2002?* | `"Nao encontrei essa informacao no documento."` |

---

## Autor

**Miguel Miranda Morandini**
- GitHub: [@miguelmorandini](https://github.com/miguelmorandini)
- LinkedIn: [Miguel Morandini](https://www.linkedin.com/in/miguel-morandini/)

---

## Licenca
Distribuido sob a licenca MIT. Consulte `LICENSE` para mais informacoes.
