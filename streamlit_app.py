"""
Databricks Technical Assistant — Interface Moderna de Chat RAG
Deploy gratuito compatível com Streamlit Community Cloud e Hugging Face Spaces.
"""

import os
import time
import json
import uuid
import streamlit as st
try:
    import chromadb
except ImportError:
    chromadb = None
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
# 2. Estilos Customizados (CSS Lakehouse Dark Edition — Design Suíço)
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
/* Tipografia e cores globais */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Sidebar Branding */
.sidebar-brand-wrapper {
    padding: 10px 0 16px 0;
    border-bottom: 1px solid #30363D;
    margin-bottom: 16px;
}

.sidebar-brand-logo {
    display: flex;
    align-items: center;
    gap: 10px;
}

.sidebar-brand-name {
    font-size: 21px;
    font-weight: 700;
    color: #F0F6FC;
    letter-spacing: -0.5px;
}

.sidebar-brand-sub {
    display: block;
    font-size: 11px;
    color: #8B949E;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 2px;
    margin-left: 36px;
    font-weight: 600;
}

/* Sidebar Section Headers */
.sidebar-section-title {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    color: #8B949E;
    margin: 18px 0 8px 0;
}

/* Status Indicators */
.status-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 500;
    margin: 6px 0 14px 0;
}

.status-connected {
    background: rgba(35, 134, 54, 0.12);
    border: 1px solid rgba(63, 185, 80, 0.25);
    color: #3FB950;
}

.status-disconnected {
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.25);
    color: #FBBF24;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #3FB950;
    box-shadow: 0 0 6px rgba(63, 185, 80, 0.8);
    display: inline-block;
}

.status-dot-warning {
    background-color: #FBBF24;
    box-shadow: 0 0 6px rgba(245, 158, 11, 0.8);
}

.status-text {
    font-size: 12px;
}

/* Base de Conhecimento Lista */
.knowledge-list {
    background: rgba(22, 27, 34, 0.5);
    border: 1px solid #30363D;
    border-radius: 8px;
    padding: 8px 12px;
    margin-bottom: 14px;
}

.knowledge-item {
    font-size: 12px;
    color: #C9D1D9;
    padding: 5px 0;
    border-bottom: 1px solid rgba(48, 54, 61, 0.4);
}

.knowledge-item:last-child {
    border-bottom: none;
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

/* Badges de Origem da Resposta */
.source-pill-local {
    display: inline-block;
    background: rgba(56, 189, 248, 0.12);
    color: #38BDF8;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 12px;
    border: 1px solid rgba(56, 189, 248, 0.25);
    margin-bottom: 8px;
}

.source-pill-online {
    display: inline-block;
    background: rgba(168, 85, 247, 0.12);
    color: #C084FC;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 12px;
    border: 1px solid rgba(168, 85, 247, 0.25);
    margin-bottom: 8px;
}

/* Card Elegante de Aviso de Cota / Rate Limit */
.rate-limit-card {
    background: rgba(245, 158, 11, 0.08);
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-radius: 12px;
    padding: 14px 18px;
    margin: 14px 0;
}

.rate-limit-badge {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    font-weight: 600;
    color: #FBBF24;
    margin-bottom: 4px;
}

.rate-limit-text {
    font-size: 12.5px;
    color: #9CA3AF;
    margin: 0;
    line-height: 1.45;
}

/* Código com JetBrains Mono */
code, pre {
    font-family: 'JetBrains Mono', Consolas, monospace !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. Gerenciamento de Conversas e Histórico em Memória
# -----------------------------------------------------------------------------
if "conversations" not in st.session_state:
    cid_inicial = f"conv_{int(time.time() * 1000)}"
    st.session_state.conversations = {
        cid_inicial: {
            "id": cid_inicial,
            "title": "Nova conversa",
            "created_at": time.time(),
            "messages": []
        }
    }
    st.session_state.current_conv_id = cid_inicial

if "current_conv_id" not in st.session_state or st.session_state.current_conv_id not in st.session_state.conversations:
    if st.session_state.conversations:
        st.session_state.current_conv_id = next(iter(st.session_state.conversations))
    else:
        cid_inicial = f"conv_{int(time.time() * 1000)}"
        st.session_state.conversations = {
            cid_inicial: {
                "id": cid_inicial,
                "title": "Nova conversa",
                "created_at": time.time(),
                "messages": []
            }
        }
        st.session_state.current_conv_id = cid_inicial

conversa_atual = st.session_state.conversations[st.session_state.current_conv_id]

# -----------------------------------------------------------------------------
# 4. Autenticação Gemini (Colab, Secrets do Streamlit ou Ambiente)
# -----------------------------------------------------------------------------
def extrair_chave(obj):
    if not obj:
        return None
    if isinstance(obj, str):
        limpa = obj.strip().strip('"').strip("'").strip()
        if len(limpa) > 10:
            return limpa
    elif isinstance(obj, dict):
        for k in ["GEMINI_API_KEY", "gemini_api_key", "api_key", "key"]:
            if k in obj:
                res = extrair_chave(obj[k])
                if res:
                    return res
        for v in obj.values():
            res = extrair_chave(v)
            if res:
                return res
    return None

def obter_api_key():
    if "api_key" in st.session_state and st.session_state["api_key"]:
        return st.session_state["api_key"]

    if hasattr(st, "secrets"):
        for k in ["GEMINI_API_KEY", "gemini_api_key", "api_key"]:
            if k in st.secrets:
                res = extrair_chave(st.secrets[k])
                if res:
                    return res
        res = extrair_chave(st.secrets)
        if res:
            return res
    
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key:
        res = extrair_chave(env_key)
        if res:
            return res
        
    return None

api_key = obter_api_key()

# -----------------------------------------------------------------------------
# 5. Sidebar: Branding Databricks, Histórico de Conversas e Metadados
# -----------------------------------------------------------------------------
with st.sidebar:
    # Logo Databricks Oficial em Vetor SVG de Alto Contraste
    st.markdown(
        """
        <div class="sidebar-brand-wrapper">
            <div class="sidebar-brand-logo">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path fill="#FF3621" d="M.95 14.184L12 20.403l9.919-5.55v2.21L12 22.662l-10.484-5.96l-.565.308v.77L12 24l11.05-6.218v-4.317l-.515-.309L12 19.118l-9.867-5.653v-2.21L12 16.805l11.05-6.218V6.32l-.515-.308L12 11.974L2.647 6.681L12 1.388l7.76 4.368l.668-.411v-.566L12 0L.95 6.27v.72L12 13.207l9.919-5.55v2.26L12 15.52L1.516 9.56l-.565.308Z"/>
                </svg>
                <span class="sidebar-brand-name">databricks</span>
            </div>
            <span class="sidebar-brand-sub">Lakehouse Assistant</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Botão para criar Nova Conversa
    if st.button("+ Nova Conversa", use_container_width=True, type="primary"):
        st.session_state.prompt_input = None
        # Se a conversa atual já possui mensagens, cria uma nova em branco
        if len(conversa_atual.get("messages", [])) > 0:
            novo_cid = f"conv_{int(time.time() * 1000)}"
            st.session_state.conversations[novo_cid] = {
                "id": novo_cid,
                "title": "Nova conversa",
                "created_at": time.time(),
                "messages": []
            }
            st.session_state.current_conv_id = novo_cid
            st.rerun()

    # Lista de Conversas Anteriores (exibe apenas conversas com histórico)
    st.markdown('<div class="sidebar-section-title">Conversas Anteriores</div>', unsafe_allow_html=True)
    
    conversas_com_historico = [
        (cid, c_data) for cid, c_data in st.session_state.conversations.items()
        if len(c_data.get("messages", [])) > 0
    ]
    
    conversas_com_historico.sort(
        key=lambda x: x[1].get("created_at", 0),
        reverse=True
    )
    
    if len(conversas_com_historico) == 0:
        st.markdown(
            '<div style="font-size: 12px; color: #8B949E; padding: 4px 0 10px 0;">Nenhuma conversa anterior ainda.</div>',
            unsafe_allow_html=True
        )
    else:
        for cid, c_data in conversas_com_historico:
            is_ativa = (cid == st.session_state.current_conv_id)
            titulo = c_data.get("title", "Conversa")
            titulo_display = titulo if len(titulo) <= 24 else titulo[:22] + "..."
            prefixo = "▸ " if is_ativa else ""
            btn_label = f"{prefixo}{titulo_display}"
            
            if st.button(
                btn_label,
                key=f"nav_conv_{cid}",
                use_container_width=True,
                type="primary" if is_ativa else "secondary"
            ):
                st.session_state.current_conv_id = cid
                st.rerun()

    # Gerenciamento da Conversa Atual
    if len(conversa_atual.get("messages", [])) > 0 or len(st.session_state.conversations) > 1:
        st.markdown('<div class="sidebar-section-title">Opções da Conversa</div>', unsafe_allow_html=True)
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            if st.button("Limpar", use_container_width=True, help="Limpa as mensagens desta conversa"):
                conversa_atual["messages"] = []
                st.rerun()
        with col_act2:
            if len(st.session_state.conversations) > 1:
                if st.button("Excluir", use_container_width=True, help="Exclui esta conversa do histórico"):
                    cid_remover = st.session_state.current_conv_id
                    del st.session_state.conversations[cid_remover]
                    st.session_state.current_conv_id = next(iter(st.session_state.conversations))
                    st.rerun()

    # Status de Conexão com Google Gemini
    st.markdown('<div class="sidebar-section-title">Status da Conexão</div>', unsafe_allow_html=True)
    if api_key:
        st.markdown(
            """
            <div class="status-badge status-connected">
                <span class="status-dot"></span>
                <span class="status-text">Google Gemini Conectado</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="status-badge status-disconnected">
                <span class="status-dot status-dot-warning"></span>
                <span class="status-text">Chave de API não informada</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        input_key = st.text_input(
            "Chave Google AI Studio:",
            type="password",
            help="Gere gratuitamente em https://aistudio.google.com/"
        )
        if input_key:
            api_key = input_key.strip().strip('"').strip("'")
            st.session_state["api_key"] = api_key
            st.rerun()

    # Base de Conhecimento Indexada
    st.markdown('<div class="sidebar-section-title">Base de Conhecimento</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="knowledge-list">
            <div class="knowledge-item">• Delta Lake Internals (ACID, Parquet)</div>
            <div class="knowledge-item">• Arquitetura Medalhão (Bronze/Silver/Gold)</div>
            <div class="knowledge-item">• Unity Catalog (3-level namespace)</div>
            <div class="knowledge-item">• Delta Live Tables (DLT Pipelines)</div>
            <div class="knowledge-item">• Performance (Photon & Liquid Clustering)</div>
            <div class="knowledge-item">• Data Warehousing (Serverless SQL)</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Links Oficiais
    st.markdown('<div class="sidebar-section-title">Documentação & Código</div>', unsafe_allow_html=True)
    st.markdown(
        "- [Databricks Documentation](https://docs.databricks.com/)\n"
        "- [Delta Lake Official](https://delta.io/)\n"
        "- [Repositório GitHub](https://github.com/miguelmorandini/chat-com-pdf)"
    )

if not api_key:
    st.info("Por favor, insira sua chave GEMINI_API_KEY no menu lateral para iniciar o assistente.")
    st.stop()

# -----------------------------------------------------------------------------
# 6. Inicialização do Cliente Gemini e ChromaDB
# -----------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def inicializar_cliente(chave):
    return genai.Client(api_key=chave)

client = inicializar_cliente(api_key)

@st.cache_resource(show_spinner=False)
def carregar_base_vetorial():
    if chromadb is None:
        return None
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection(
        name="databricks_knowledge_base",
        metadata={"hnsw:space": "cosine"}
    )
    
    if collection.count() == 0:
        docs_dir = "data/databricks_docs"
        if os.path.exists(docs_dir):
            chunks_iniciais = []
            for f in os.listdir(docs_dir):
                if f.endswith(".md"):
                    with open(os.path.join(docs_dir, f), "r", encoding="utf-8") as arq:
                        conteudo = arq.read()
                        titulo = f.replace(".md", "").replace("_", " ").title()
                        for i in range(0, len(conteudo), 700):
                            trecho = conteudo[i:i + 850].strip()
                            if len(trecho) > 60:
                                chunks_iniciais.append({
                                    "titulo": f"Databricks Concept - {titulo}",
                                    "url": f"https://docs.databricks.com/aws/en/ (Módulo: {f})",
                                    "texto": trecho
                                })
            
            if chunks_iniciais:
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
except Exception:
    collection = None

# -----------------------------------------------------------------------------
# 7. Funções RAG e Consulta com Fallback
# -----------------------------------------------------------------------------
MODELOS_LLM = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-2.0-flash-lite"
]

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

def executar_geracao_llm(prompt):
    """
    Executa a geração com tratamento inteligente de stream, backoff e fallback robusto de modelos.
    Apenas modelos homologados e disponíveis na API gratuita são acionados.
    """
    erros_por_modelo = {}
    
    # 1. Tenta streaming testando a resposta inicial de cada modelo com backoff automático
    for modelo in MODELOS_LLM:
        for tentativa in range(2):
            try:
                stream = client.models.generate_content_stream(
                    model=modelo,
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.2)
                )
                primeiro_chunk = next(stream)
                
                def gerador_protegido():
                    if primeiro_chunk and primeiro_chunk.text:
                        yield primeiro_chunk.text
                    try:
                        for chunk in stream:
                            if chunk and chunk.text:
                                yield chunk.text
                    except Exception:
                        pass

                return gerador_protegido(), True, ""
            except Exception as e:
                err_str = str(e)
                erros_por_modelo[modelo] = err_str
                if any(cod in err_str for cod in ["429", "503", "RESOURCE_EXHAUSTED", "overloaded"]):
                    time.sleep(1.2 * (tentativa + 1))
                else:
                    break
            
    # 2. Se o streaming falhar em todos, tenta chamada direta convencional com cada modelo
    for modelo in MODELOS_LLM:
        try:
            resp = client.models.generate_content(
                model=modelo,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.2)
            )
            if resp and resp.text:
                return resp.text.strip(), True, ""
        except Exception as e:
            erros_por_modelo[f"{modelo}_sync"] = str(e)
            continue

    # Formata relatório consolidado
    linhas_erro = []
    for m, err in erros_por_modelo.items():
        resumo = err.splitlines()[0] if err else "Erro desconhecido"
        if len(resumo) > 120:
            resumo = resumo[:118] + "..."
        linhas_erro.append(f"• {m}: {resumo}")
    relatorio_erros = "\n".join(linhas_erro)

    return None, False, relatorio_erros

def processar_pergunta(pergunta, historico=None):
    trechos = buscar_documentos_locais(pergunta)
    eh_local = len(trechos) > 0
    
    # Extrai o contexto das mensagens anteriores para manter a memória do diálogo
    bloco_historico = ""
    if historico:
        turnos = []
        for h in historico[-6:]:
            papel = "Usuário" if h.get("role") == "user" else "Assistente"
            txt = h.get("content", "").strip()
            if len(txt) > 300:
                txt = txt[:300] + "..."
            turnos.append(f"{papel}: {txt}")
        if turnos:
            bloco_historico = "HISTÓRICO RECENTE DA CONVERSA:\n" + "\n".join(turnos) + "\n\n"

    if eh_local:
        contexto = "\n\n".join([
            f"[Fonte: {t['titulo']} | Link: {t['url']}]\n{t['texto']}"
            for t in trechos
        ])
        fontes_utilizadas = [{"titulo": t["titulo"], "url": t["url"]} for t in trechos]
        origem = "local"
        prompt = f"""
Você é o Databricks Assistant, um especialista sênior em Engenharia de Dados no ecossistema Databricks.
Responda à pergunta do usuário utilizando como base técnica sólida as informações do CONTEXTO e considerando o HISTÓRICO da conversa quando o usuário fizer perguntas de continuação.

Diretrizes:
1. Responda em português com linguagem técnica, precisa, estruturada e didática.
2. Explique os termos fundamentais com clareza (ex: o que é uma pipeline de dados, Delta Live Tables, streaming, etc.).
3. Se o assunto envolver código, forneça exemplos limpos em SQL ou PySpark.
4. Se a pergunta for totalmente fora do escopo de dados, tecnologia ou Databricks (ex: futebol, culinária), recuse educadamente dizendo:
   "Não encontrei essa informação na documentação oficial da Databricks."

{bloco_historico}CONTEXTO:
{contexto}

PERGUNTA ATUAL:
{pergunta}
"""
    else:
        origem = "docs"
        fontes_utilizadas = [{"titulo": "Databricks Official Documentation", "url": "https://docs.databricks.com/"}]
        prompt = f"""
Você é o Databricks Assistant, especialista sênior em Engenharia de Dados no ecossistema Databricks.
Responda à pergunta técnica do usuário com base rigorosa na documentação oficial da Databricks (docs.databricks.com) e considerando o HISTÓRICO da conversa quando o usuário fizer perguntas de continuação.

Diretrizes:
1. Responda em português de forma completa, didática e estruturada.
2. Explique os conceitos fundamentais e como o Databricks os resolve.
3. Se relevante, forneça exemplos em PySpark ou Databricks SQL.
4. Cite seções oficiais de docs.databricks.com correspondentes.
5. Se for fora do escopo de tecnologia e Databricks (ex: futebol, receitas), responda estritamente:
   "Não encontrei essa informação na documentação oficial da Databricks."

{bloco_historico}PERGUNTA ATUAL:
{pergunta}
"""

    conteudo, sucesso, erro = executar_geracao_llm(prompt)
    return {
        "conteudo": conteudo,
        "sucesso": sucesso,
        "erro": erro,
        "origem": origem,
        "fontes": fontes_utilizadas
    }

# -----------------------------------------------------------------------------
# 8. Layout Principal: Header e Histórico do Chat Atual
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="header-container">
        <span class="online-pill">docs.databricks.com</span>
        <span class="brand-badge">Lakehouse Assistant</span>
        <h1 class="header-title">Databricks Technical Assistant</h1>
        <p class="header-desc">
            Assistente RAG especializado em Engenharia de Dados, Delta Lake, Unity Catalog, 
            Delta Live Tables, Ingestão Contínua e Otimização com Photon.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

mensagens = conversa_atual.get("messages", [])

# Verifica se há prompt pendente (seja de botão de sugestão ou de chat_input)
tem_prompt_pendente = ("prompt_input" in st.session_state and bool(st.session_state.prompt_input))

# Sugestões Rápidas (Exibidas se a conversa atual estiver sem mensagens e nenhuma pergunta tiver sido clicada)
if len(mensagens) == 0 and not tem_prompt_pendente:
    st.markdown("##### Perguntas Sugeridas")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Camadas da Arquitetura Medalhão", use_container_width=True):
            st.session_state.prompt_input = "Qual a responsabilidade de cada camada (Bronze, Silver e Gold) na arquitetura Medalhão?"
            st.rerun()
        if st.button("Unity Catalog vs Hive Metastore", use_container_width=True):
            st.session_state.prompt_input = "Como funciona o namespace de três níveis no Unity Catalog e quais as vantagens sobre o Hive Metastore?"
            st.rerun()
    with col2:
        if st.button("Liquid Clustering no Delta Lake", use_container_width=True):
            st.session_state.prompt_input = "Como funciona o recurso de Liquid Clustering no Databricks e quando substitui o particionamento?"
            st.rerun()
        if st.button("Declarative Pipelines no DLT", use_container_width=True):
            st.session_state.prompt_input = "O que são Spark Declarative Pipelines no Delta Live Tables (DLT)?"
            st.rerun()

# Renderiza histórico de mensagens da conversa atual
for msg in mensagens:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="⚡"):
            texto_limpo = msg["content"]
            if "⏳ A API do Google Gemini está com limite" in texto_limpo:
                texto_limpo = texto_limpo.split("⏳ A API do Google Gemini")[0].strip()
            texto_limpo = texto_limpo.replace("🌐 [Especialista Databricks Docs]\n\n", "").strip()
            texto_limpo = texto_limpo.replace("📚 [Base de Conhecimento Local]\n\n", "").strip()

            origem = msg.get("origem", "docs")
            if origem == "local":
                st.markdown('<span class="source-pill-local">Base Local (ChromaDB)</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="source-pill-online">Documentação Oficial Databricks</span>', unsafe_allow_html=True)
                
            st.markdown(texto_limpo)
            if "fontes" in msg and msg["fontes"]:
                with st.expander("Fontes Oficiais Consultadas", expanded=False):
                    for f in msg["fontes"]:
                        st.markdown(f"- [{f['titulo']}]({f['url']})")

# -----------------------------------------------------------------------------
# 9. Entrada do Usuário e Geração Dinâmica
# -----------------------------------------------------------------------------
prompt_usuario = st.chat_input("Pergunte sobre Delta Lake, Unity Catalog, DLT, SQL Warehouses...")

if "prompt_input" in st.session_state and st.session_state.prompt_input:
    prompt_usuario = st.session_state.prompt_input
    st.session_state.prompt_input = None

if prompt_usuario:
    # 1. Captura o histórico atual para fornecer contexto conversacional contínuo ao assistente
    historico_previo = list(conversa_atual.get("messages", []))

    # 2. Se for a primeira mensagem, define o título com base na pergunta
    if conversa_atual.get("title") == "Nova conversa":
        titulo_gerado = prompt_usuario.strip()
        if len(titulo_gerado) > 28:
            titulo_gerado = titulo_gerado[:26] + "..."
        conversa_atual["title"] = titulo_gerado

    # 3. Registra e renderiza mensagem do usuário
    conversa_atual["messages"].append({"role": "user", "content": prompt_usuario})

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt_usuario)

    # 4. Executa a geração assistente considerando o histórico
    with st.chat_message("assistant", avatar="⚡"):
        res = processar_pergunta(prompt_usuario, historico=historico_previo)
        
        if res["sucesso"] and res["conteudo"] is not None:
            if res["origem"] == "local":
                st.markdown('<span class="source-pill-local">Base Local (ChromaDB)</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="source-pill-online">Documentação Oficial Databricks</span>', unsafe_allow_html=True)
                
            texto_gerado = ""
            try:
                if hasattr(res["conteudo"], "__iter__") and not isinstance(res["conteudo"], str):
                    texto_gerado = st.write_stream(res["conteudo"])
                else:
                    texto_gerado = res["conteudo"]
                    st.markdown(texto_gerado)
                    
                if res.get("fontes"):
                    with st.expander("Fontes Oficiais Consultadas", expanded=False):
                        for f in res["fontes"]:
                            st.markdown(f"- [{f['titulo']}]({f['url']})")
                            
                conversa_atual["messages"].append({
                    "role": "assistant",
                    "content": texto_gerado,
                    "origem": res["origem"],
                    "fontes": res.get("fontes", [])
                })
            except Exception as e_stream:
                st.markdown(
                    """
                    <div class="rate-limit-card">
                        <div class="rate-limit-badge">
                            <span>⏳</span> Limite Temporário de Requisições
                        </div>
                        <p class="rate-limit-text">
                            A conexão com a API gratuita da Google foi interrompida ou atingiu a cota por minuto.<br>
                            Por favor, aguarde cerca de 15 a 30 segundos para a janela resetar e tente novamente.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            # Remove a mensagem de usuário da lista permanente caso não tenha obtido resposta
            if conversa_atual["messages"] and conversa_atual["messages"][-1]["role"] == "user":
                conversa_atual["messages"].pop()

            erro_detalhe = str(res.get("erro", ""))
            eh_chave_invalida = any(k in erro_detalhe for k in ["API_KEY_INVALID", "API key not valid", "400 INVALID_ARGUMENT"])
            eh_rate_limit = any(k in erro_detalhe for k in ["429", "RESOURCE_EXHAUSTED", "quota", "overloaded", "503"])

            if eh_chave_invalida:
                st.markdown(
                    """
                    <div class="rate-limit-card" style="border-color: rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.08);">
                        <div class="rate-limit-badge" style="color: #F87171;">
                            <span>⚠️</span> Chave Gemini Não Reconhecida
                        </div>
                        <p class="rate-limit-text">
                            A chave de API informada é inválida ou expirou.<br>
                            Verifique se a chave em <strong>Settings > Secrets</strong> ou no menu lateral está correta.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            elif eh_rate_limit:
                st.markdown(
                    """
                    <div class="rate-limit-card">
                        <div class="rate-limit-badge">
                            <span>⏳</span> Cota Temporária Atingida (Rate Limit do Google AI Studio)
                        </div>
                        <p class="rate-limit-text">
                            A chave gratuita do Google AI Studio atingiu o limite de 15 requisições por minuto.<br>
                            <strong>Aguarde cerca de 20 a 30 segundos</strong> para a janela de 1 minuto da Google resetar e clique em tentar novamente.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div class="rate-limit-card">
                        <div class="rate-limit-badge">
                            <span>⚠️</span> Servidores da Google Temporariamente Indisponíveis
                        </div>
                        <p class="rate-limit-text">
                            Os modelos da Google não responderam no momento.<br>
                            Aguarde alguns segundos e clique em tentar novamente.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            col_retry, _ = st.columns([1, 2])
            with col_retry:
                if st.button("🔄 Tentar Novamente", key=f"retry_{int(time.time()*1000)}", use_container_width=True):
                    st.session_state.prompt_input = prompt_usuario
                    st.rerun()

            if erro_detalhe:
                with st.expander("Ver detalhes do erro", expanded=False):
                    st.code(erro_detalhe)
