"""
Gera assets visuais em alta resolução para a apresentação do Chat com PDF & Databricks RAG.
"""

import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = "presentation/assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

FONT_DIR = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
font_sans = os.path.join(FONT_DIR, "segoeui.ttf")
font_sans_bold = os.path.join(FONT_DIR, "segoeuib.ttf")
font_mono = os.path.join(FONT_DIR, "consola.ttf")

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

# ==============================================================================
# 1. LOGO TRANSPARENTE OFICIAL: rag_logo.png (1000 x 280)
# ==============================================================================
def create_logo():
    w, h = 1000, 280
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Simbolo: Spark + Camadas RAG
    cx, cy = 130, 140
    # Glow de fundo
    for r in range(80, 20, -5):
        alpha = int(25 * (1 - r / 80))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 210, 255, alpha))

    # Desenhar documento inferior (ChromaDB / Databricks)
    draw.rounded_rectangle([cx - 48, cy - 25, cx + 25, cy + 50], radius=8, fill=(255, 84, 54, 230), outline=(255, 120, 90, 255), width=2)
    # Desenhar documento intermediário (TF-IDF / PDF)
    draw.rounded_rectangle([cx - 36, cy - 38, cx + 38, cy + 38], radius=8, fill=(26, 115, 232, 240), outline=(66, 145, 255, 255), width=2)
    # Desenhar documento frontal (Gemini Spark)
    draw.rounded_rectangle([cx - 22, cy - 50, cx + 52, cy + 25], radius=8, fill=(13, 19, 34, 250), outline=(0, 210, 255, 255), width=2)

    # Spark icon dentro do documento frontal
    sp_cx, sp_cy = cx + 15, cy - 12
    sp_pts = [
        (sp_cx, sp_cy - 18),
        (sp_cx + 5, sp_cy - 5),
        (sp_cx + 18, sp_cy),
        (sp_cx + 5, sp_cy + 5),
        (sp_cx, sp_cy + 18),
        (sp_cx - 5, sp_cy + 5),
        (sp_cx - 18, sp_cy),
        (sp_cx - 5, sp_cy - 5),
    ]
    draw.polygon(sp_pts, fill=(0, 210, 255, 255))

    # Tipografia do Logo
    f_title = get_font(font_sans_bold, 54)
    f_sub = get_font(font_sans, 24)
    f_pill = get_font(font_mono, 18)

    tx = 240
    draw.text((tx, 70), "Chat com PDF", font=f_title, fill=(255, 255, 255, 255))
    draw.text((tx + 360, 86), "RAG", font=f_title, fill=(0, 210, 255, 255))

    draw.text((tx, 142), "Sistemas RAG com Google Gemini & Databricks Knowledge Base", font=f_sub, fill=(203, 213, 225, 255))
    draw.text((tx, 178), "by Miguel Miranda Morandini", font=f_sub, fill=(148, 163, 184, 255))

    # Badge Pill
    draw.rounded_rectangle([tx, 214, tx + 430, 246], radius=6, fill=(16, 24, 45, 200), outline=(0, 210, 255, 120), width=1)
    draw.text((tx + 12, 218), "ZERO ALUCINACAO • 100% CITACAO DE PAGINAS", font=f_pill, fill=(0, 210, 255, 255))

    img.save(os.path.join(ASSETS_DIR, "rag_logo.png"), "PNG")
    print("rag_logo.png criada com sucesso!")

# ==============================================================================
# 2. SLIDE 2: legacy_search_problem.png (1200 x 680)
# ==============================================================================
def create_problem_diagram():
    w, h = 1200, 680
    img = Image.new("RGBA", (w, h), (7, 10, 19, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(font_sans_bold, 28)
    f_sub = get_font(font_sans, 18)
    f_body = get_font(font_sans, 16)
    f_mono = get_font(font_mono, 15)

    # Painel 1: O Velho Ctrl+F (Busca Tradicional)
    draw.rounded_rectangle([50, 50, 570, 500], radius=12, fill=(19, 27, 46, 255), outline=(255, 255, 255, 30), width=1)
    draw.rounded_rectangle([70, 70, 280, 105], radius=6, fill=(255, 84, 54, 30), outline=(255, 84, 54, 120), width=1)
    draw.text((85, 78), "01. BUSCA TRADICIONAL", font=f_mono, fill=(255, 84, 54, 255))
    draw.text((70, 125), "O Dilema do 'Ctrl + F'", font=f_title, fill=(255, 255, 255, 255))

    items_left = [
        ("Termos Isolados:", "Encontra palavras exatas sem entender contexto ou sinonimos."),
        ("Zero Sintese:", "Nao responde perguntas; joga 500 paginas para leitura manual."),
        ("Silos de Dados:", "Incapaz de correlacionar capitulos ou tabelas distintas."),
        ("Resultado:", "Engenheiro perde horas folheando PDFs e manuais extensos.")
    ]
    y = 185
    for label, desc in items_left:
        draw.text((70, y), label, font=get_font(font_sans_bold, 16), fill=(255, 120, 90, 255))
        draw.text((70, y + 24), desc, font=f_body, fill=(203, 213, 225, 255))
        y += 65

    # Painel 2: O LLM Puro sem Grounding
    draw.rounded_rectangle([630, 50, 1150, 500], radius=12, fill=(19, 27, 46, 255), outline=(255, 255, 255, 30), width=1)
    draw.rounded_rectangle([650, 70, 920, 105], radius=6, fill=(245, 158, 11, 30), outline=(245, 158, 11, 120), width=1)
    draw.text((665, 78), "02. LLM SEM GROUNDING", font=f_mono, fill=(245, 158, 11, 255))
    draw.text((650, 125), "A Armadilha da Alucinacao", font=f_title, fill=(255, 255, 255, 255))

    items_right = [
        ("Eloquencia Enganosa:", "Inventa fatos com seguranca impecavel quando nao sabe."),
        ("Corte Temporal:", "Desconhece manuais internos e mudancas tecnicas recentes."),
        ("Zero Auditoria:", "Nao fornece pagina ou paragrafo de onde a resposta veio."),
        ("Resultado:", "Risco critico de producao e perda de confianca da equipe.")
    ]
    y = 185
    for label, desc in items_right:
        draw.text((650, y), label, font=get_font(font_sans_bold, 16), fill=(255, 209, 102, 255))
        draw.text((650, y + 24), desc, font=f_body, fill=(203, 213, 225, 255))
        y += 65

    # Faixa inferior de Solucao: RAG
    draw.rounded_rectangle([50, 530, 1150, 630], radius=10, fill=(26, 115, 232, 35), outline=(0, 210, 255, 150), width=1)
    draw.text((75, 550), "A SOLUCAO: RETRIEVAL-AUGMENTED GENERATION (RAG)", font=f_mono, fill=(0, 210, 255, 255))
    draw.text((75, 580), "Unir a velocidade da busca vetorial com a inteligencia de sintese do Gemini — citando paginas e garantindo zero invencoes.", font=f_sub, fill=(255, 255, 255, 255))

    img.save(os.path.join(ASSETS_DIR, "legacy_search_problem.png"), "PNG")
    print("legacy_search_problem.png criada com sucesso!")

# ==============================================================================
# 3. SLIDE 3: rag_interface_verified.png (1280 x 740)
# ==============================================================================
def create_interface_screenshot():
    w, h = 1280, 740
    img = Image.new("RGBA", (w, h), (9, 14, 26, 255))
    draw = ImageDraw.Draw(img)

    f_app_title = get_font(font_sans_bold, 24)
    f_sub = get_font(font_sans, 15)
    f_bold = get_font(font_sans_bold, 15)
    f_body = get_font(font_sans, 14)
    f_mono = get_font(font_mono, 13)

    # Top App Header (Gradio Style)
    draw.rectangle([0, 0, w, 65], fill=(7, 10, 19, 255), outline=(255, 255, 255, 25), width=1)
    draw.text((30, 18), "Chat com PDF — Assistente RAG com Google Gemini", font=f_app_title, fill=(255, 255, 255, 255))
    draw.rounded_rectangle([w - 180, 16, w - 30, 48], radius=6, fill=(16, 185, 129, 30), outline=(16, 185, 129, 180), width=1)
    draw.text((w - 165, 24), "ONLINE • v2.4", font=f_mono, fill=(16, 185, 129, 255))

    # Coluna Esquerda: Upload & Status (400px)
    draw.rounded_rectangle([30, 90, 420, 700], radius=10, fill=(15, 22, 38, 255), outline=(255, 255, 255, 25), width=1)
    draw.text((50, 110), "DOCUMENTO ATIVO", font=f_mono, fill=(0, 210, 255, 255))
    
    # Box do Arquivo
    draw.rounded_rectangle([50, 140, 400, 270], radius=8, fill=(10, 15, 28, 255), outline=(0, 210, 255, 80), width=1)
    draw.text((70, 160), "The-Delta-Lake-Series-Lakehouse-012921.pdf", font=f_bold, fill=(255, 255, 255, 255))
    draw.text((70, 188), "Tamanho: 869 KB • 19 Paginas extraidas", font=f_body, fill=(148, 163, 184, 255))
    draw.text((70, 212), "Chunking: 800 caracteres / 150 overlap", font=f_mono, fill=(203, 213, 225, 255))
    draw.text((70, 236), "Indexador: TF-IDF (43 chunks uteis)", font=f_mono, fill=(0, 210, 255, 255))

    # Botao de Re-indexar
    draw.rounded_rectangle([50, 290, 400, 335], radius=6, fill=(26, 115, 232, 255))
    draw.text((155, 302), "Indexar Novo PDF", font=f_bold, fill=(255, 255, 255, 255))

    # Box de Metricas do Documento
    draw.rounded_rectangle([50, 360, 400, 680], radius=8, fill=(10, 15, 28, 255), outline=(255, 255, 255, 20), width=1)
    draw.text((70, 380), "METRICAS DE INDEXACAO", font=f_mono, fill=(255, 209, 102, 255))
    
    metrics = [
        ("Paginas Processadas:", "19 paginas"),
        ("Paginas Filtradas:", "1, 2, 4, 10, 15 (capas/vazias)"),
        ("Chunks Relevantes:", "43 blocos com metadados"),
        ("Matriz Esparsa:", "43 x 1.428 n-gramas"),
        ("Latencia de Busca:", "14 ms (em memoria RAM)"),
        ("Status de Confiabilidade:", "100% Grounded (Auditoria OK)")
    ]
    my = 415
    for k, v in metrics:
        draw.text((70, my), k, font=f_mono, fill=(148, 163, 184, 255))
        draw.text((70, my + 18), v, font=f_bold, fill=(255, 255, 255, 255))
        my += 42

    # Coluna Direita: Chat Interface (790px)
    draw.rounded_rectangle([450, 90, 1250, 700], radius=10, fill=(15, 22, 38, 255), outline=(255, 255, 255, 25), width=1)
    
    # Mensagem do Usuario
    draw.rounded_rectangle([720, 120, 1220, 180], radius=10, fill=(26, 115, 232, 220))
    draw.text((740, 130), "Usuario:", font=f_mono, fill=(255, 255, 255, 200))
    draw.text((740, 150), "What is Delta Lake and how does it bring reliability?", font=f_bold, fill=(255, 255, 255, 255))

    # Resposta do Gemini (Grounded)
    draw.rounded_rectangle([480, 205, 1220, 520], radius=10, fill=(10, 15, 28, 255), outline=(0, 210, 255, 100), width=1)
    draw.text((505, 225), "Gemini 3.5 Flash-Lite (Assistente Fundamentado):", font=f_mono, fill=(0, 210, 255, 255))
    
    resp_lines = [
        "Com base exclusivamente no documento 'The Delta Lake Series - Lakehouse':",
        "",
        "1. Sistema Unificado de Gestao: O Delta Lake e um sistema unificado que traz confiabilidade",
        "   e alta performance analitica diretamente sobre 'data lakes' em nuvem (Pagina 3).",
        "",
        "2. Transacoes ACID com Parquet: Ele implementa uma camada de armazenamento ACID aberta",
        "   utilizando um Log de Transacoes serializavel e arquivos no formato Apache Parquet (Pagina 8).",
        "",
        "3. Compatibilidade Spark: E 100% compativel com as APIs do Apache Spark, permitindo unificar",
        "   cargas de trabalho em batch (lote) e streaming com garantias de isolamento (Paginas 3 e 8).",
        "",
        "Fontes auditadas no documento: Pagina 3 e Pagina 8."
    ]
    ry = 260
    for line in resp_lines:
        color = (255, 209, 102, 255) if "Fontes auditadas" in line else (203, 213, 225, 255)
        draw.text((505, ry), line, font=f_body, fill=color)
        ry += 22

    # Segunda Mensagem: Teste Negativo (Anti-Alucinacao)
    draw.rounded_rectangle([720, 535, 1220, 590], radius=10, fill=(26, 115, 232, 220))
    draw.text((740, 545), "Usuario:", font=f_mono, fill=(255, 255, 255, 200))
    draw.text((740, 565), "Quem foi o campeao mundial de futebol em 2002?", font=f_bold, fill=(255, 255, 255, 255))

    draw.rounded_rectangle([480, 605, 1220, 675], radius=10, fill=(10, 15, 28, 255), outline=(16, 185, 129, 120), width=1)
    draw.text((505, 618), "Gemini 3.5 Flash-Lite (Regra de Recusa Ativada):", font=f_mono, fill=(16, 185, 129, 255))
    draw.text((505, 642), '"Nao encontrei essa informacao no documento."', font=f_bold, fill=(255, 255, 255, 255))

    img.save(os.path.join(ASSETS_DIR, "rag_interface_verified.png"), "PNG")
    print("rag_interface_verified.png criada com sucesso!")

# ==============================================================================
# 4. SLIDE 6: incremental_pipeline.png (1200 x 680)
# ==============================================================================
def create_pipeline_diagram():
    w, h = 1200, 680
    img = Image.new("RGBA", (w, h), (7, 10, 19, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(font_sans_bold, 24)
    f_step = get_font(font_mono, 14)
    f_body = get_font(font_sans, 15)
    f_mono = get_font(font_mono, 13)

    # Titulo Superior
    draw.text((50, 40), "PIPELINE DE INGESTAO INCREMENTAL DATABRICKS", font=get_font(font_sans_bold, 28), fill=(255, 255, 255, 255))
    draw.text((50, 80), "Estrategia de Hashing SHA-256 e Deteccao de Mudancas sem Desperdicio de Tokens", font=f_body, fill=(148, 163, 184, 255))

    # 4 Blocos em Sequencia Horizontal
    blocos = [
        ("01. SITEMAP OFICIAL", "docs.databricks.com/sitemap.xml", [
            "Varredura de URLs oficiais",
            "Filtro regex de 8 dominios-chave",
            "(Lakehouse, Delta, Unity Catalog)",
            "Descarta release-notes e arquivos"
        ], (26, 115, 232)),
        ("02. HASHING SHA-256", "data/ingestion_state.json", [
            "Download do HTML e extracao",
            "Calculo de fingerprint SHA-256",
            "Compara com hash salvo",
            "Hash igual = 0 TOKENS (Skip)"
        ], (16, 185, 129)),
        ("03. BATCH EMBEDDINGS", "gemini-embedding-001", [
            "Apenas chunks modificados",
            "Envio em lotes otimizados",
            "Reducao de 90% em HTTP calls",
            "Fallback automatico por item"
        ], (0, 210, 255)),
        ("04. CHROMA & CI/CD", "GitHub Actions Semanal", [
            "Upsert atomico no ChromaDB",
            "Cron aos domingos as 03:00 UTC",
            "Compactacao em chroma_db.tar.gz",
            "Auto-commit no repositorio Git"
        ], (255, 84, 54))
    ]

    bx = 50
    for title, subtitle, bullets, col in blocos:
        draw.rounded_rectangle([bx, 130, bx + 250, 480], radius=10, fill=(15, 22, 38, 255), outline=col + (150,), width=2)
        draw.rounded_rectangle([bx + 15, 145, bx + 235, 175], radius=6, fill=col + (30,), outline=col + (120,), width=1)
        draw.text((bx + 25, 152), title, font=f_step, fill=col + (255,))
        draw.text((bx + 15, 195), subtitle, font=f_mono, fill=(203, 213, 225, 255))

        by = 240
        for b in bullets:
            draw.text((bx + 15, by), "• " + b, font=f_mono, fill=(255, 255, 255, 255) if "0 TOKENS" in b else (148, 163, 184, 255))
            by += 38

        # Seta para a direita se nao for o ultimo
        if bx < 850:
            draw.polygon([(bx + 262, 305), (bx + 262, 295), (bx + 278, 300)], fill=(0, 210, 255, 200))

        bx += 280

    # Faixa de Impacto
    draw.rounded_rectangle([50, 520, 1150, 630], radius=10, fill=(10, 15, 28, 255), outline=(16, 185, 129, 150), width=1)
    draw.text((75, 540), "RESULTADO DE ENGENHARIA: CONSUMO DE TOKENS EM PRODUCAO", font=f_step, fill=(16, 185, 129, 255))
    draw.text((75, 570), "Em varreduras semanais com 50 paginas onde apenas 2 sofreram alteracao na Databricks:", font=f_body, fill=(203, 213, 225, 255))
    draw.text((75, 595), "96% das paginas tem CACHE HIT imediato -> 0 tokens gastos de embeddings -> Custo e latencia reduzidos em 95%.", font=get_font(font_sans_bold, 16), fill=(0, 210, 255, 255))

    img.save(os.path.join(ASSETS_DIR, "incremental_pipeline.png"), "PNG")
    print("incremental_pipeline.png criada com sucesso!")

# ==============================================================================
# 5. SLIDE 8: sdd_architecture.png (1200 x 680)
# ==============================================================================
def create_sdd_diagram():
    w, h = 1200, 680
    img = Image.new("RGBA", (w, h), (7, 10, 19, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(font_sans_bold, 28)
    f_step = get_font(font_mono, 14)
    f_body = get_font(font_sans, 15)
    f_mono = get_font(font_mono, 13)

    draw.text((50, 40), "ENGENHARIA ORIENTADA A ESPECIFICACOES (SDD)", font=f_title, fill=(255, 255, 255, 255))
    draw.text((50, 80), "Separação Estrita de Responsabilidades, Contratos de Dados e Testes Contínuos", font=f_body, fill=(148, 163, 184, 255))

    # 3 Camadas de Arquitetura
    camadas = [
        ("01. CONTRATOS DE DADOS", [
            ("Chunk Size: 800", "Garante coerencia semantica completa de paragrafos"),
            ("Overlap: 150", "Elimina perda de contexto nas fronteiras de corte"),
            ("Metadata Standard", "Titulo, URL e Pagina preservados em 100% dos chunks"),
            ("Page Exclusion Rule", "Ignora capas e paginas vazias (ex: 1, 2, 4, 10, 15)")
        ]),
        ("02. MODULARIDADE LIMPA", [
            ("src/ingest_pipeline.py", "Sitemap scraping, SHA-256 e ChromaDB upsert"),
            ("app.py", "Indexacao TF-IDF em memoria e interface Gradio"),
            ("Prompt Shield", "Isolamento da persona e regra mandatoria de recusa"),
            ("Chroma Local Tarball", "Versionamento compacto e seguro no GitHub Actions")
        ]),
        ("03. TESTES AUTOMATIZADOS", [
            ("test_chunking_and_metadata", "Valida que tamanho e URLs sao respeitados"),
            ("test_hash_calculation", "Garante determinismo do SHA-256 para textos iguais"),
            ("Unittest / Pytest Pass", "2/2 testes passando com 0 falhas em CI/CD"),
            ("Zero Codigo Morto", "Cada modulo atende a um requisito real do sistema")
        ])
    ]

    bx = 50
    for title, items in camadas:
        draw.rounded_rectangle([bx, 130, bx + 345, 600], radius=10, fill=(15, 22, 38, 255), outline=(0, 210, 255, 80), width=1)
        draw.rounded_rectangle([bx + 15, 145, bx + 330, 175], radius=6, fill=(26, 115, 232, 40), outline=(26, 115, 232, 120), width=1)
        draw.text((bx + 25, 152), title, font=f_step, fill=(0, 210, 255, 255))

        iy = 200
        for label, desc in items:
            draw.text((bx + 20, iy), label, font=get_font(font_sans_bold, 15), fill=(255, 255, 255, 255))
            draw.text((bx + 20, iy + 22), desc, font=f_mono, fill=(148, 163, 184, 255))
            iy += 88

        bx += 385

    img.save(os.path.join(ASSETS_DIR, "sdd_architecture.png"), "PNG")
    print("sdd_architecture.png criada com sucesso!")

if __name__ == "__main__":
    create_logo()
    create_problem_diagram()
    create_interface_screenshot()
    create_pipeline_diagram()
    create_sdd_diagram()
    print("Todos os assets visuais gerados com perfeicao!")
