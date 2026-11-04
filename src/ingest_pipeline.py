"""
Pipeline de Ingestao Incremental da Documentacao Oficial da Databricks.
Varre o sitemap.xml, detecta alteracoes com SHA-256 e indexa vetores no ChromaDB com gemini-embedding-001.
"""

import os
import re
import json
import time
import hashlib
import argparse
import urllib.request
from html.parser import HTMLParser

SITEMAP_URL = "https://docs.databricks.com/sitemap.xml"
STATE_FILE = "data/ingestion_state.json"
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "databricks_knowledge_base"

# Topicos aprovados de Engenharia de Dados
TOPICOS_INCLUIDOS = [
    "/lakehouse/",
    "/delta/",
    "/data-governance/",
    "/ingestion/",
    "/delta-live-tables/",
    "/optimizations/",
    "/pyspark/",
    "/sql/"
]

TOPICOS_EXCLUIDOS = [
    "/archive/",
    "/release-notes/",
    "/error-messages/",
    "/admin/account-settings"
]

class DatabricksDocParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_article = False
        self.in_script = False
        self.text_parts = []
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in ["script", "style", "nav", "footer", "header", "noscript"]:
            self.in_script = True
        if tag in ["article", "main"]:
            self.in_article = True
        if tag == "title":
            self.in_title = True
        if tag in ["h1", "h2", "h3", "p", "li"]:
            self.text_parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ["script", "style", "nav", "footer", "header", "noscript"]:
            self.in_script = False
        if tag in ["article", "main"]:
            self.in_article = False
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data.strip()
        if self.in_article and not self.in_script:
            self.text_parts.append(data)

def extrair_pagina(url):
    """Baixa e extrai conteudo textual e titulo de uma URL da Databricks."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8")

        parser = DatabricksDocParser()
        parser.feed(html)
        texto_bruto = "".join(parser.text_parts)
        linhas = [linha.strip() for linha in texto_bruto.split("\n") if linha.strip()]
        texto_limpo = "\n".join(linhas)

        titulo = parser.title.replace(" | Databricks on AWS", "").replace(" | Databricks", "").strip()
        return {
            "url": url,
            "titulo": titulo or url,
            "conteudo": texto_limpo,
            "hash": hashlib.sha256(texto_limpo.encode("utf-8")).hexdigest()
        }
    except Exception as e:
        print(f"Aviso: Falha ao baixar {url}: {e}")
        return None

def obter_urls_do_sitemap():
    """Baixa o sitemap.xml da Databricks e filtra pelas categorias de Engenharia de Dados."""
    print("Buscando sitemap oficial em docs.databricks.com/sitemap.xml...")
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(SITEMAP_URL, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read().decode("utf-8")

    todas_urls = re.findall(r"<loc>(https://docs\.databricks\.com/aws/en/[^<]+)</loc>", content)
    print(f"Total de URLs encontradas no sitemap: {len(todas_urls)}")

    urls_filtradas = []
    for u in todas_urls:
        if any(exc in u for exc in TOPICOS_EXCLUIDOS):
            continue
        if any(inc in u for inc in TOPICOS_INCLUIDOS):
            urls_filtradas.append(u)

    print(f"URLs selecionadas para Engenharia de Dados: {len(urls_filtradas)}")
    return urls_filtradas

def criar_chunks(doc, tamanho=900, overlap=120):
    """Divide o conteudo da pagina em chunks contextuais com metadados."""
    chunks = []
    texto = doc["conteudo"]
    url = doc["url"]
    titulo = doc["titulo"]
    passo = tamanho - overlap

    for inicio in range(0, max(1, len(texto)), passo):
        trecho = texto[inicio:inicio + tamanho].strip()
        if len(trecho) > 60:
            chunks.append({
                "titulo": titulo,
                "url": url,
                "texto": trecho
            })
    return chunks

def carregar_estado():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"last_run": None, "total_pages": 0, "pages": {}}

def salvar_estado(estado):
    os.makedirs(os.path.dirname(STATE_FILE) or ".", exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(estado, f, indent=2, ensure_ascii=False)

def gerar_embeddings_lote(client, lista_textos, max_tentativas=3):
    """Gera embeddings em lote para otimizar chamadas a API do Gemini."""
    for tentativa in range(max_tentativas):
        try:
            resp = client.models.embed_content(
                model="gemini-embedding-001",
                contents=lista_textos
            )
            return [emb.values for emb in resp.embeddings]
        except Exception as e:
            if tentativa < max_tentativas - 1:
                time.sleep(2 * (tentativa + 1))
            else:
                raise e

def executar_pipeline(max_pages=50, dry_run=False, force=False):
    print("=" * 70)
    print("INICIANDO PIPELINE DE INGESTAO INCREMENTAL DATABRICKS")
    print("=" * 70)

    estado = carregar_estado()
    urls = obter_urls_do_sitemap()

    if max_pages:
        urls = urls[:max_pages]

    print(f"\nProcessando ate {len(urls)} paginas...")
    paginas_para_indexar = []
    paginas_puladas = 0

    for idx, u in enumerate(urls, start=1):
        # Verifica se pagina foi modificada
        doc = extrair_pagina(u)
        if not doc or len(doc["conteudo"]) < 100:
            continue

        ultimo_hash = estado.get("pages", {}).get(u, {}).get("hash")
        if not force and ultimo_hash == doc["hash"]:
            paginas_puladas += 1
            continue

        paginas_para_indexar.append(doc)
        print(f"[{idx}/{len(urls)}] Modificada/Nova: {doc['titulo']}")
        time.sleep(0.05)

    print(f"\nResumo da verificacao:")
    print(f"- Paginas inalteradas (puladas sem custo): {paginas_puladas}")
    print(f"- Paginas que exigem indexacao: {len(paginas_para_indexar)}")

    if dry_run:
        print("\n[Modo Dry-Run]: Nenhuma alteracao foi feita no ChromaDB nem na API.")
        return

    if not paginas_para_indexar:
        print("\nBase de conhecimento ja esta 100% atualizada! Nada a fazer.")
        return

    # Autenticacao Gemini
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Configure a variavel GEMINI_API_KEY antes de rodar a indexacao.")
    
    from google import genai
    import chromadb
    client = genai.Client(api_key=api_key)

    # Inicializa ChromaDB
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    # Processamento e geracao de chunks
    todos_chunks = []
    for doc in paginas_para_indexar:
        chunks_doc = criar_chunks(doc)
        todos_chunks.extend(chunks_doc)

    print(f"\nGerando embeddings para {len(todos_chunks)} chunks em lotes...")
    tamanho_lote = 25  # Lotes para respeitar o tamanho maximo de requisicao
    total_processados = 0

    for i in range(0, len(todos_chunks), tamanho_lote):
        lote = todos_chunks[i:i + tamanho_lote]
        textos_completos = [
            f"Titulo: {c['titulo']} | URL: {c['url']}\n{c['texto']}"
            for c in lote
        ]

        vetores = gerar_embeddings_lote(client, textos_completos)

        ids = [f"doc_{hashlib.md5(c['url'].encode()).hexdigest()[:8]}_{i + j}" for j, c in enumerate(lote)]
        documents = [c["texto"] for c in lote]
        metadatas = [{"titulo": c["titulo"], "url": c["url"]} for c in lote]

        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=vetores
        )

        total_processados += len(lote)
        print(f"Progresso: {total_processados}/{len(todos_chunks)} chunks gravados no ChromaDB.")
        time.sleep(0.5)

    # Atualiza registro de estado
    agora = time.strftime("%Y-%m-%d %H:%M:%S")
    estado["last_run"] = agora
    for doc in paginas_para_indexar:
        estado["pages"][doc["url"]] = {
            "hash": doc["hash"],
            "titulo": doc["titulo"],
            "last_updated": agora
        }
    estado["total_pages"] = len(estado["pages"])
    salvar_estado(estado)

    print(f"\nPipeline concluido com sucesso!")
    print(f"Total de registros na colecao ChromaDB: {collection.count()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline Incremental Databricks Docs")
    parser.add_argument("--max-pages", type=int, default=50, help="Numero maximo de paginas a verificar")
    parser.add_argument("--dry-run", action="store_true", help="Apenas simula a checagem sem chamar API ou gravar no banco")
    parser.add_argument("--force", action="store_true", help="Forca reindexacao mesmo se os hashes forem iguais")
    args = parser.parse_args()

    executar_pipeline(max_pages=args.max_pages, dry_run=args.dry_run, force=args.force)
