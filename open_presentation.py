"""
Script auxiliar para abrir a Apresentação Técnica do Projeto Chat com PDF & Databricks RAG.
Abre o arquivo presentation/index.html diretamente no navegador padrão.
"""

import webbrowser
from pathlib import Path

def main():
    presentation_file = Path(__file__).parent / "presentation" / "index.html"
    if presentation_file.exists():
        url = presentation_file.resolve().as_uri()
        print(f"[Chat com PDF] Abrindo apresentacao tecnica: {url}")
        webbrowser.open(url)
    else:
        print(f"[ERRO] Arquivo de apresentacao nao encontrado em: {presentation_file}")

if __name__ == "__main__":
    main()
