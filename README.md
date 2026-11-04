# 📄 Chat com PDF — IA Generativa & RAG

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/miguelmorandini/chat-com-pdf/blob/main/chat_com_pdf.ipynb)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-GenAI%20SDK-orange?logo=google)
![Gradio](https://img.shields.io/badge/UI-Gradio-ff7c00?logo=gradio)
![License](https://img.shields.io/badge/License-MIT-green)

Um assistente inteligente de perguntas e respostas baseado em documentos PDF utilizando a arquitetura **RAG (Retrieval-Augmented Generation)** com a API do **Google Gemini** e interface interativa via **Gradio**.

O projeto resolve o desafio de **eliminar alucinações** em modelos generativos ao responder sobre documentos corporativos e técnicos, garantindo que as respostas sejam embasadas exclusivamente no texto fornecido e citando expressamente a numeração das páginas consultadas.

---

## 🎯 Objetivo & Requisitos do Projeto

- **Ambiente Universal:** Executável tanto no **Google Colab** quanto em ambiente local.
- **Extração Precisa:** Preservação do mapeamento de página durante a extração do PDF com `PyPDF2`.
- **Chunking Semântico:** Segmentação em blocos com *overlap* (sobreposição) para não fragmentar conceitos.
- **Recuperação Relevante:** Busca textual por similaridade de cosseno via **TF-IDF** (`scikit-learn`).
- **Engenharia de Prompt Anti-Alucinação:** Diretrizes explícitas para impedir deduções infundadas e forçar a citação das páginas.
- **Entregáveis Validados:** 
  - 3 perguntas técnicas respondidas com sucesso com citação de página.
  - 1 pergunta fora de escopo respondida categoricamente com: *"Não encontrei essa informação no documento."*

---

## 🧠 Arquitetura do Pipeline RAG

```
                 +-----------------------------------------+
                 |            Documento PDF                |
                 +-----------------------------------------+
                                      |
                                      v
                 +-----------------------------------------+
                 |    1. Extração por Página (PyPDF2)      |
                 +-----------------------------------------+
                                      |
                                      v
                 +-----------------------------------------+
                 |    2. Chunking com Overlap (800 / 150)  |
                 +-----------------------------------------+
                                      |
                                      v
                 +-----------------------------------------+
                 |   3. Matriz TF-IDF & Índice Vetorial    |
                 +-----------------------------------------+
                                      |
 Pergunta do Usuário  --------------->+ (Similaridade de Cosseno)
                                      |
                                      v
                 +-----------------------------------------+
                 |     Top-k Trechos Relevantes + Páginas  |
                 +-----------------------------------------+
                                      |
                                      v
                 +-----------------------------------------+
                 | 4. Prompt Anti-Alucinação + Contexto     |
                 +-----------------------------------------+
                                      |
                                      v
                 +-----------------------------------------+
                 |    5. Google Gemini (API GenAI)         |
                 +-----------------------------------------+
                                      |
                                      v
                 +-----------------------------------------+
                 | Resposta com Citação da Página (Gradio) |
                 +-----------------------------------------+
```

---

## 🚀 Como Executar

### Opção 1: Diretamente no Google Colab
Basta clicar no botão abaixo para abrir e rodar o notebook na nuvem sem necessidade de configuração prévia:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/miguelmorandini/chat-com-pdf/blob/main/chat_com_pdf.ipynb)

> **Dica:** Adicione sua chave gratuita do Google AI Studio no menu lateral do Colab (**Secrets** / Ícone de chave) com o nome `GEMINI_API_KEY`.

---

### Opção 2: Localmente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/miguelmorandini/chat-com-pdf.git
   cd chat-com-pdf
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv .venv
   # No Windows:
   .venv\Scripts\activate
   # No Linux/Mac:
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Defina sua chave de API:**
   ```bash
   # Windows (PowerShell)
   $env:GEMINI_API_KEY="sua_chave_aqui"

   # Linux/Mac
   export GEMINI_API_KEY="sua_chave_aqui"
   ```

5. **Inicie o Jupyter Notebook ou a aplicação:**
   ```bash
   jupyter notebook chat_com_pdf.ipynb
   ```

---

## 🧪 Bateria de Testes (Critérios de Aceite)

| Tipo de Teste | Pergunta | Comportamento Esperado |
| :--- | :--- | :--- |
| **Pergunta Técnica 1** | *What is Delta Lake and how does it bring reliability?* | Resposta precisa citando as páginas (ex: Pág. 3 e 8) |
| **Pergunta Técnica 2** | *What is a Lakehouse and what problems does it solve?* | Resumo conceitual citando a Pág. 6 |
| **Pergunta Técnica 3** | *How does Delta Lake handle ACID transactions?* | Explicação do Transaction Log citando a Pág. 8 e 13 |
| **Teste Anti-Alucinação** | *Qual é a escalação da seleção brasileira em 2002?* | `"Não encontrei essa informação no documento."` |

---

## 🔮 Próximas Evoluções (Roadmap de Aprendizado)

- [ ] **Embeddings Densos:** Substituir o TF-IDF por modelos de embeddings neurais (`text-embedding-004` da Google).
- [ ] **Vector Database:** Integrar com banco vetorial persistente (ChromaDB ou FAISS).
- [ ] **Multi-Documentos:** Permitir indexar uma pasta inteira com múltiplos PDFs simultâneos.
- [ ] **Hybrid Search:** Combinação de busca esparsa (BM25) e densa (Embeddings) com re-ranking.
- [ ] **Exportação para API:** Criar endpoints REST usando FastAPI para integração em outros sistemas.

---

## 👤 Autor

**Miguel Miranda Morandini**
- GitHub: [@miguelmorandini](https://github.com/miguelmorandini)
- LinkedIn: [Miguel Morandini](https://www.linkedin.com/in/miguel-morandini/)

---

## 📄 Licença
Distribuído sob a licença MIT. Consulte `LICENSE` para mais informações.
