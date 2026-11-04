# Projetos de RAG com Google Gemini

Este repositorio reune duas abordagens complementares de aplicacao da arquitetura **RAG (Retrieval-Augmented Generation)** com o **Google Gemini**:

1. **[Chat com PDF](chat_com_pdf.ipynb):** Implementacao leve e direta para responder perguntas sobre documentos em PDF utilizando PyPDF2 e TF-IDF (Desafio Inicial).
2. **[Assistente Databricks](databricks_rag_assistant.ipynb):** Plataforma avancada de RAG multi-documentos utilizando a documentacao tecnica oficial de Databricks, com **ChromaDB** e **Google Embeddings (`text-embedding-004`)**.

---

## Notebooks Disponiveis

| Notebook | Foco | Recuperacao | Armazenamento | LLM | Abrir no Colab |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`chat_com_pdf.ipynb`** | PDF Unico (Delta Lake eBook) | TF-IDF + Cosseno | Em memoria | `gemini-3.5-flash-lite` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/miguelmorandini/chat-com-pdf/blob/main/chat_com_pdf.ipynb) |
| **`databricks_rag_assistant.ipynb`** | Multi-Docs (Databricks Knowledge Base) | Embeddings Semanticos | ChromaDB Local | `gemini-3.5-flash-lite` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/miguelmorandini/chat-com-pdf/blob/main/databricks_rag_assistant.ipynb) |

---

## 1. Chat com PDF (Desafio Inicial)

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
