"""
Chat com PDF — Aplicação RAG com Google Gemini e Gradio
Permite conversar com documentos PDF com mitigação de alucinação e citação de páginas.
"""

import os
import numpy as np
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from google import genai
import gradio as gr

# 1. Autenticação Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    try:
        from google.colab import userdata
        api_key = userdata.get("GEMINI_API_KEY")
    except Exception:
        pass

# Trata se api_key for um dicionário ou JSON
if isinstance(api_key, dict):
    for k in ["GEMINI_API_KEY", "api_key", "key", "token"]:
        if k in api_key and isinstance(api_key[k], str):
            api_key = api_key[k]
            break
    else:
        for v in api_key.values():
            if isinstance(v, str):
                api_key = v
                break

if isinstance(api_key, str):
    api_key = api_key.strip()
    if api_key.startswith("{") and api_key.endswith("}"):
        try:
            import json
            dados = json.loads(api_key)
            if isinstance(dados, dict):
                for k in ["GEMINI_API_KEY", "api_key", "key", "token"]:
                    if k in dados and isinstance(dados[k], str):
                        api_key = dados[k].strip()
                        break
                else:
                    for v in dados.values():
                        if isinstance(v, str):
                            api_key = v.strip()
                            break
        except Exception:
            pass

client = genai.Client(api_key=api_key) if (api_key and isinstance(api_key, str)) else None

# Estado global da indexação
indice = {
    "chunks": [],
    "matriz": None,
    "vectorizer": None,
    "arquivo": None
}

def extrair_e_indexar(pdf_path):
    """Lê o PDF, quebra em chunks e indexa com TF-IDF."""
    if not pdf_path:
        return "Nenhum arquivo fornecido."
    
    reader = PdfReader(pdf_path)
    paginas = []
    for num, pag in enumerate(reader.pages, start=1):
        txt = pag.extract_text() or ""
        paginas.append({"pagina": num, "texto": txt.strip()})

    # Chunking com overlap
    chunks = []
    tamanho, overlap = 800, 150
    passo = tamanho - overlap
    for pag in paginas:
        texto = " ".join(pag["texto"].split())
        for i in range(0, len(texto), passo):
            trecho = texto[i:i + tamanho]
            if len(trecho.strip()) > 30:
                chunks.append({"pagina": pag["pagina"], "texto": trecho})

    if not chunks:
        return "Nenhum texto legível encontrado no PDF."

    # TF-IDF (exclui capas/títulos sem densidade e chunks muito curtos)
    PAGINAS_EXCLUIDAS = {1, 2, 4, 10, 15, 19}
    chunks_uteis = [c for c in chunks if c["pagina"] not in PAGINAS_EXCLUIDAS and len(c["texto"].split()) > 15]
    if not chunks_uteis:
        chunks_uteis = [c for c in chunks if len(c["texto"].split()) > 15]

    if not chunks_uteis:
        return "Nenhum texto legível encontrado no PDF."

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
    matriz = vectorizer.fit_transform([c["texto"] for c in chunks_uteis])

    indice["chunks"] = chunks_uteis
    indice["matriz"] = matriz
    indice["vectorizer"] = vectorizer
    indice["arquivo"] = os.path.basename(pdf_path)

    return f"Documento '{indice['arquivo']}' indexado com sucesso ({len(chunks_uteis)} chunks gerados de {len(paginas)} paginas)."

def perguntar_pdf(pergunta):
    """Pipeline RAG anti-alucinação."""
    if not client:
        return "Erro: Configure a variável de ambiente GEMINI_API_KEY antes de continuar."
    if not indice["chunks"]:
        return "Por favor, carregue e indexe um PDF antes de fazer perguntas."

    vetor = indice["vectorizer"].transform([pergunta])
    scores = cosine_similarity(vetor, indice["matriz"]).ravel()
    indices_top = np.argsort(scores)[::-1][:5]

    resultados = [
        indice["chunks"][int(i)]
        for i in indices_top
        if scores[i] > 0
    ]

    if not resultados:
        return "Não encontrei essa informação no documento."

    contexto = "\n\n".join(
        f"[Página {r['pagina']}]\n{r['texto']}"
        for r in resultados
    )

    prompt = f"""
Você é um assistente que responde perguntas
exclusivamente com base em documentos.

Regras:
- Utilize somente as informações do contexto.
- Não invente informações.
- Cite as páginas utilizadas.
- Responda em português de forma clara, completa e detalhada.
- Caso não encontre a resposta, diga estritamente:
  "Não encontrei essa informação no documento."

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}
"""
    try:
        resp = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )
        return resp.text.strip()
    except Exception as e:
        return f"Erro ao consultar Gemini: {e}"

# Auto-indexa sample.pdf se estiver presente na pasta
if os.path.exists("sample.pdf"):
    extrair_e_indexar("sample.pdf")

def chat_fn(mensagem, historico):
    if not mensagem.strip():
        return "Digite uma pergunta válida."
    return perguntar_pdf(mensagem)

with gr.Blocks(title="Chat com PDF - Assistente RAG") as demo:
    gr.Markdown("# Chat com PDF - Assistente RAG com Google Gemini")
    gr.Markdown("Faca upload de qualquer PDF para tirar duvidas tecnicas. As respostas citam as paginas de referencia e evitam alucinacoes.")
    
    with gr.Row():
        with gr.Column(scale=1):
            pdf_input = gr.File(label="Upload de PDF", file_types=[".pdf"])
            btn_processar = gr.Button("Indexar Documento", variant="primary")
            status_txt = gr.Textbox(
                label="Status",
                value=f"Documento padrão carregado: {indice['arquivo']}" if indice['arquivo'] else "Nenhum arquivo carregado",
                interactive=False
            )
            btn_processar.click(extrair_e_indexar, inputs=[pdf_input], outputs=[status_txt])
        
        with gr.Column(scale=2):
            chat = gr.ChatInterface(
                fn=chat_fn,
                examples=[
                    "What is Delta Lake?",
                    "What is a Lakehouse architecture?",
                    "Quem foi campeão mundial de futebol em 2002?"
                ]
            )

if __name__ == "__main__":
    demo.launch(share=False)
