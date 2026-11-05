"""
Databricks Technical Assistant — Interface Moderna de Chat RAG
Deploy gratuito compatível com Streamlit Community Cloud e Hugging Face Spaces.
"""

import os
import time
import json
import streamlit as st
import chromadb
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# 1. Configuração da Página e Metadados
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Databricks AI Assistant",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. Estilos Customizados (CSS Lakehouse Dark Edition)
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
/* Fonte e cores de fundo */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header estilizado */
.header-container {
    background: linear-gradient(135deg, rgba(22, 27, 34, 0.95), rgba(13, 17, 23, 0.98));
    border: 1px solid rgba(255, 54, 33, 0.25);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 25px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
}

.brand-badge {
    display: inline-block;
    background: rgba(255, 54, 33, 0.12);
    color: #FF5A43;
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid rgba(255, 54, 33, 0.3);
    margin-bottom: 10px;
}

.online-pill {
    display: inline-block;
    background: rgba(35, 134, 54, 0.15);
    color: #3fb950;
    font-size: 11px;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 12px;
    border: 1px solid rgba(63, 185, 80, 0.3);
    float: right;
}

.header-title {
    font-size: 26px;
    font-weight: 700;
    color: #F0F6FC;
    margin: 0;
    letter-spacing: -0.5px;
}

.header-desc {
    color: #8B949E;
    font-size: 14px;
    margin-top: 6px;
    line-height: 1.5;
}

/* Sugestões rápidas (Quick Pills) */
.pill-btn {
    display: inline-block;
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 20px;
    padding: 8px 16px;
    font-size: 13px;
    color: #C9D1D9;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.2s ease;
    margin: 4px;
}
.pill-btn:hover {
    border-color: #FF3621;
    color: #FFFFFF;
    background: rgba(255, 54, 33, 0.08);
}

/* Estilo para citações de fontes */
.source-box {
    background: rgba(22, 27, 34, 0.7);
    border-left: 3px solid #00A3E0;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    font-size: 12px;
    color: #8B949E;
    margin-top: 12px;
}

/* Código com JetBrains Mono */
code, pre {
    font-family: 'JetBrains Mono', Consolas, monospace !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. Autenticação Gemini (Colab, Secrets do Streamlit ou Ambiente)
# -----------------------------------------------------------------------------
def obter_api_key():
    # 1. Tenta dos secrets do Streamlit Cloud
    if hasattr(st, "secrets"):
        for k in ["GEMINI_API_KEY", "gemini_api_key", "api_key"]:
            if k in st.secrets:
                val = st.secrets[k]
                if isinstance(val, str) and len(val.strip()) > 10:
                    return val.strip().strip('"').strip("'")
    
    # 2. Tenta das variáveis de ambiente
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key and len(env_key.strip()) > 10:
        return env_key.strip().strip('"').strip("'")
        
    return None

api_key = obter_api_key()

# -----------------------------------------------------------------------------
# 4. Sidebar: Configurações, Status e Metadados
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/63/Databricks_Logo.png", width=180)
    st.markdown("### ⚙️ Painel de Controle")
    
    # Se a chave não foi encontrada no ambiente/secrets, oferece input seguro
    if not api_key:
        st.warning("🔑 Chave GEMINI_API_KEY não detectada nos secrets.")
        input_key = st.text_input(
            "Insira sua chave do Google AI Studio:",
            type="password",
            help="Gere gratuitamente em https://aistudio.google.com/"
        )
        if input_key:
            api_key = input_key.strip().strip('"').strip("'")
            st.session_state["api_key"] = api_key
            st.rerun()
    else:
        st.success("🟢 Chave Google Gemini Conectada", icon="✅")
    
    st.markdown("---")
    st.markdown("#### 📚 Base Técnica Indexada")
    st.markdown(
        "- **Delta Lake Internals** (ACID, Parquet)\n"
        "- **Arquitetura Medalhão** (Bronze/Silver/Gold)\n"
        "- **Unity Catalog** (3-level namespace)\n"
        "- **Delta Live Tables** (Declarative Pipelines)\n"
        "- **Performance** (Photon & Liquid Clustering)\n"
        "- **Data Warehousing** (Serverless SQL)"
    )
    st.markdown("---")
    
    if st.button("🧹 Limpar Histórico de Conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown(
        "🔗 **Links Oficiais:**\n"
        "- [Databricks Docs](https://docs.databricks.com/)\n"
        "- [Delta Lake Official](https://delta.io/)\n"
        "- [Repositório GitHub](https://github.com/miguelmorandini/chat-com-pdf)"
    )

if not api_key:
    st.info("👈 Por favor, insira sua `GEMINI_API_KEY` na barra lateral esquerda para iniciar o chat.", icon="🔑")
    st.stop()

# -----------------------------------------------------------------------------
# 5. Inicialização do Cliente Gemini e ChromaDB
# -----------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def inicializar_cliente(chave):
    return genai.Client(api_key=chave)

client = inicializar_cliente(api_key)

@st.cache_resource(show_spinner=False)
def carregar_base_vetorial():
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection(
        name="databricks_knowledge_base",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Se o banco estiver vazio, carrega os documentos essenciais de data/databricks_docs
    if collection.count() == 0:
        docs_dir = "data/databricks_docs"
        if os.path.exists(docs_dir):
            chunks_iniciais = []
            for f in os.listdir(docs_dir):
                if f.endswith(".md"):
                    with open(os.path.join(docs_dir, f), "r", encoding="utf-8") as arq:
                        conteudo = arq.read()
                        titulo = f.replace(".md", "").replace("_", " ").title()
                        # Segmenta em trechos de ~800 caracteres
                        for i in range(0, len(conteudo), 700):
                            trecho = conteudo[i:i + 850].strip()
                            if len(trecho) > 60:
                                chunks_iniciais.append({
                                    "titulo": f"Databricks Concept - {titulo}",
                                    "url": f"https://docs.databricks.com/aws/en/ (Módulo: {f})",
                                    "texto": trecho
                                })
            
            if chunks_iniciais:
                # Gera embeddings com gemini-embedding-001
                vetores = []
                docs_validos = []
                metas = []
                ids = []
                for idx, c in enumerate(chunks_iniciais):
                    try:
                        resp = client.models.embed_content(
                            model="gemini-embedding-001",
                            contents=f"Titulo: {c['titulo']}\n{c['texto']}"
                        )
                        if resp.embeddings and len(resp.embeddings) > 0:
                            vetores.append(resp.embeddings[0].values)
                            docs_validos.append(c["texto"])
                            metas.append({"titulo": c["titulo"], "url": c["url"]})
                            ids.append(f"init_chunk_{idx}")
                    except Exception:
                        pass
                
                if vetores:
                    collection.upsert(ids=ids, documents=docs_validos, metadatas=metas, embeddings=vetores)
                    
    return collection

try:
    collection = carregar_base_vetorial()
except Exception as e:
    collection = None

# -----------------------------------------------------------------------------
# 6. Funções RAG e Consulta com Fallback
# -----------------------------------------------------------------------------
MODELOS_LLM = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-3.5-flash-lite"]

def buscar_documentos_locais(pergunta, top_k=4):
    if collection is None:
        return []
    try:
        resp = client.models.embed_content(model="gemini-embedding-001", contents=pergunta)
        if not resp.embeddings or len(resp.embeddings) == 0:
            return []
        vetor = resp.embeddings[0].values
        res = collection.query(query_embeddings=[vetor], n_results=top_k)
        
        resultados = []
        if res.get("documents") and len(res["documents"][0]) > 0:
            for i in range(len(res["documents"][0])):
                dist = res["distances"][0][i] if "distances" in res else 0.5
                if dist < 0.88:
                    meta = res["metadatas"][0][i] if res.get("metadatas") else {}
                    resultados.append({
                        "texto": res["documents"][0][i],
                        "titulo": meta.get("titulo", "Databricks Documentation"),
                        "url": meta.get("url", "https://docs.databricks.com/aws/en/"),
                        "distancia": dist
                    })
        return resultados
    except Exception:
        return []

def gerar_resposta_stream(pergunta, historico):
    trechos = buscar_documentos_locais(pergunta)
    
    eh_local = len(trechos) > 0
    fontes_utilizadas = []
    
    if eh_local:
        contexto = "\n\n".join([
            f"[Fonte: {t['titulo']} | Link: {t['url']}]\n{t['texto']}"
            for t in trechos
        ])
        fontes_utilizadas = [{"titulo": t["titulo"], "url": t["url"]} for t in trechos]
        prompt = f"""
Você é o Databricks Assistant, um especialista sênior em Engenharia de Dados no ecossistema Databricks.
Responda à pergunta do usuário utilizando como base técnica sólida as informações do CONTEXTO abaixo.

Diretrizes:
1. Responda em português com linguagem técnica, precisa, estruturada e didática.
2. Explique os termos fundamentais com clareza (ex: o que é uma pipeline de dados, Delta Live Tables, streaming, etc.).
3. Se o assunto envolver código, forneça exemplos limpos em SQL ou PySpark.
4. Se a pergunta for totalmente fora do escopo de dados, tecnologia ou Databricks (ex: futebol, culinária), recuse educadamente dizendo:
   "Não encontrei essa informação na documentação oficial da Databricks."

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}
"""
    else:
        # Fallback Especialista Online
        prompt = f"""
Você é o Databricks Assistant, especialista sênior em Engenharia de Dados no ecossistema Databricks.
Responda à pergunta técnica do usuário com base rigorosa na documentação oficial da Databricks (docs.databricks.com).

Diretrizes:
1. Responda em português de forma completa, didática e estruturada.
2. Explique os conceitos fundamentais e como o Databricks os resolve.
3. Se relevante, forneça exemplos em PySpark ou Databricks SQL.
4. Cite seções oficiais de docs.databricks.com correspondentes.
5. Se for fora do escopo de tecnologia e Databricks (ex: futebol, receitas), responda estritamente:
   "Não encontrei essa informação na documentação oficial da Databricks."

PERGUNTA:
{pergunta}
"""
        fontes_utilizadas = [{"titulo": "Databricks Official Documentation", "url": "https://docs.databricks.com/"}]

    # Executa a geração em streaming
    for modelo in MODELOS_LLM:
        try:
            stream = client.models.generate_content_stream(
                model=modelo,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.2)
            )
            
            # Prefixo com badge de origem
            if eh_local:
                yield "📚 **[Base de Conhecimento Local]**\n\n"
            else:
                yield "🌐 **[Especialista Databricks Docs]**\n\n"
                
            for chunk in stream:
                if chunk and chunk.text:
                    yield chunk.text
            return
        except Exception:
            continue
            
    yield "⏳ A API do Google Gemini está com limite temporário de requisições. Por favor, aguarde alguns segundos e tente novamente."

# -----------------------------------------------------------------------------
# 7. Layout Principal: Header e Pílulas Rápidas
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="header-container">
        <span class="online-pill">🟢 docs.databricks.com</span>
        <span class="brand-badge">⚡ Lakehouse AI Assistant</span>
        <h1 class="header-title">Databricks Technical Assistant</h1>
        <p class="header-desc">
            Assistente RAG especializado em Engenharia de Dados, Delta Lake, Unity Catalog, 
            Delta Live Tables, Ingestão Contínua e Otimização com Photon.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Inicializa o histórico na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sugestões Rápidas (Exibidas se o chat estiver vazio)
if len(st.session_state.messages) == 0:
    st.markdown("##### 💡 Perguntas Sugeridas:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏗️ Camadas da Arquitetura Medalhão", use_container_width=True):
            st.session_state.prompt_input = "Qual a responsabilidade de cada camada (Bronze, Silver e Gold) na arquitetura Medalhão?"
        if st.button("🛡️ Unity Catalog vs Hive Metastore", use_container_width=True):
            st.session_state.prompt_input = "Como funciona o namespace de três níveis no Unity Catalog e quais as vantagens sobre o Hive Metastore?"
    with col2:
        if st.button("⚡ Como funciona o Liquid Clustering?", use_container_width=True):
            st.session_state.prompt_input = "Como funciona o recurso de Liquid Clustering no Databricks e quando substitui o particionamento?"
        if st.button("🔄 O que são Declarative Pipelines?", use_container_width=True):
            st.session_state.prompt_input = "O que são Spark Declarative Pipelines no Delta Live Tables (DLT)?"

# -----------------------------------------------------------------------------
# 8. Renderização do Histórico do Chat
# -----------------------------------------------------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="⚡"):
            st.markdown(msg["content"])
            if "fontes" in msg and msg["fontes"]:
                with st.expander("📖 Fontes Oficiais Consultadas", expanded=False):
                    for f in msg["fontes"]:
                        st.markdown(f"- [{f['titulo']}]({f['url']})")

# -----------------------------------------------------------------------------
# 9. Entrada do Usuário e Geração Dinâmica
# -----------------------------------------------------------------------------
prompt_usuario = st.chat_input("Pergunte sobre Delta Lake, Unity Catalog, DLT, SQL Warehouses...")

# Trata se veio de um botão de sugestão rápida
if "prompt_input" in st.session_state and st.session_state.prompt_input:
    prompt_usuario = st.session_state.prompt_input
    st.session_state.prompt_input = None

if prompt_usuario:
    # 1. Registra e exibe a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt_usuario})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt_usuario)

    # 2. Gera a resposta com streaming dinâmico
    with st.chat_message("assistant", avatar="⚡"):
        resposta_completa = st.write_stream(gerar_resposta_stream(prompt_usuario, st.session_state.messages))
        
        # Registra no histórico da sessão
        st.session_state.messages.append({
            "role": "assistant",
            "content": resposta_completa
        })
