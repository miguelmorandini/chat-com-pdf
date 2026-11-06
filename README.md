# Projetos de RAG com Google Gemini

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chat-com-pdf.streamlit.app)
[![GitHub license](https://img.shields.io/github/license/miguelmorandini/chat-com-pdf)](LICENSE)

Este repositorio reune duas abordagens complementares de aplicacao da arquitetura **RAG (Retrieval-Augmented Generation)** com o **Google Gemini**:

1. **[Chat com PDF](chat_com_pdf.ipynb):** Implementacao leve e direta para responder perguntas sobre documentos em PDF utilizando PyPDF2 e TF-IDF (Desafio Inicial).
2. **[Assistente Databricks](databricks_rag_assistant.ipynb):** Plataforma avancada de RAG multi-documentos utilizando a documentacao tecnica oficial de Databricks, com **ChromaDB** e **Google Embeddings (`gemini-embedding-001`)**.
3. **[Databricks Technical Assistant (Web App)](streamlit_app.py):** Interface conversacional moderna completa com streaming, historico de chats persistente e design Lakehouse, hospedada gratuitamente em produção no Streamlit Cloud: **[https://chat-com-pdf.streamlit.app](https://chat-com-pdf.streamlit.app)**.

---

## 🚀 Aplicacao Web em Producao (Deploy Online Gratuito)

Acesse o assistente em tempo real diretamente no seu navegador, sem necessidade de instalar nada:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chat-com-pdf.streamlit.app)

👉 **Link Direto:** **[https://chat-com-pdf.streamlit.app](https://chat-com-pdf.streamlit.app)**

- **Streaming em Tempo Real:** Respostas digitadas progressivamente na tela com `st.write_stream`.
- **Memoria Conversacional Multi-Turnos:** Mantem o contexto das perguntas anteriores para dialogos tecnicos fluidos.
- **Historico Persistente na Barra Lateral:** Permite iniciar novas conversas (`+ Nova Conversa`) e navegar entre chats passados.
- **Descoberta Dinamica de Modelos:** Roteamento automatico entre modelos ativos da Google (`client.models.list()`) com protecao resiliente de cotas.

---

## Notebooks e Aplicacoes Disponiveis

| Projeto / Notebook | Foco | Recuperacao | Armazenamento | LLM | Acesso Online |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`databricks_rag_assistant.ipynb`** | Multi-Docs (Databricks Knowledge Base) | Embeddings Semanticos | ChromaDB Local | Google Gemini | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/miguelmorandini/chat-com-pdf/blob/main/databricks_rag_assistant.ipynb) [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chat-com-pdf.streamlit.app) |
| **`chat_com_pdf.ipynb`** | PDF Unico (Delta Lake eBook) | TF-IDF + Cosseno | Em memoria | Google Gemini | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/miguelmorandini/chat-com-pdf/blob/main/chat_com_pdf.ipynb) |
| **`streamlit_app.py`** | Web App Completa (Deploy Nuvem) | RAG Hibrido + Fallback | ChromaDB / Memoria | Descoberta Dinamica | [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chat-com-pdf.streamlit.app) |

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
   # Opção A: Executar o app web moderno de Chat Databricks (Streamlit):
   streamlit run streamlit_app.py

   # Opção B: Executar o app Gradio original (Chat com PDF):
   python app.py

   # Opção C: Abrir os notebooks interativos:
   jupyter notebook databricks_rag_assistant.ipynb
   ```

---

## 2. Assistente Databricks & Pipeline de Ingestao Contínua

O segundo projeto (`databricks_rag_assistant.ipynb`) conta com um **pipeline de ingestao incremental automatizado** (`src/ingest_pipeline.py`) que mantem a base de conhecimento sempre sincronizada com o site oficial da Databricks:

- **Fonte Oficial:** Leitura automatica do sitemap oficial (`https://docs.databricks.com/sitemap.xml`), cobrindo Lakehouse, Delta Lake, Unity Catalog, Delta Live Tables, Ingestao, Otimizacoes, PySpark e SQL.
- **Detecção de Mudanças (SHA-256):** Compara o hash do texto de cada pagina com `data/ingestion_state.json`. Paginas inalteradas sao ignoradas (0 tokens consumidos).
- **Batch Embeddings:** Envia chunks em lotes com `gemini-embedding-001`, reduzindo chamadas a API em ate 90%.
- **Fallback Inteligente com Grounding Oficial (Zero Custo):** Quando o usuario pergunta sobre topicos que ainda nao estao na base local (ChromaDB), o assistente aciona automaticamente o Google Search Grounding restrito a `docs.databricks.com`, garantindo respostas precisas e links oficiais em tempo real sem custo no plano gratuito.
- **Automacao Semanal no GitHub Actions:** O workflow `.github/workflows/sync_databricks_docs.yml` roda autonomamente todo domingo as 03:00 UTC, atualizando o banco vetorial e salvando as alteracoes no repositorio.

### Como executar o pipeline de ingestao manualmente:
```bash
# Simular a varredura sem gastar tokens (dry-run):
python src/ingest_pipeline.py --dry-run --max-pages 20

# Executar a ingestao real de 50 paginas:
python src/ingest_pipeline.py --max-pages 50
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

## Apresentacao Tecnica (Deck de Slides de 10 min)

O repositorio inclui um deck de slides interativo em HTML5/CSS3/JS, estruturado especificamente para uma apresentacao tecnica de ate 10 minutos (incluindo cronometro integrado, notas do apresentador, visao geral em grade e controle por teclado):

```bash
# Abrir a apresentacao tecnica no navegador padrao:
python open_presentation.py
```
> O arquivo tambem pode ser aberto diretamente via [`presentation/index.html`](presentation/index.html) ou clicando duas vezes em `presentation/open_presentation.bat`.  
> O roteiro verbal com minutagem detalhada esta documentado em [`presentation/ROTEIRO_APRESENTACAO.md`](presentation/ROTEIRO_APRESENTACAO.md).

---

## Autor

**Miguel Miranda Morandini**
- GitHub: [@miguelmorandini](https://github.com/miguelmorandini)
- LinkedIn: [Miguel Morandini](https://www.linkedin.com/in/miguel-morandini/)

---

## Licenca
Distribuido sob a licenca MIT. Consulte `LICENSE` para mais informacoes.
