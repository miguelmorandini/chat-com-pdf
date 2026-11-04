# Arquitetura Medalhao no Databricks Lakehouse

A arquitetura medalhao e um padrao de design de dados que organiza os dados em camadas sequenciais de refinamento e qualidade a medida que fluem pelo lakehouse. O objetivo e fornecer estrutura, confiabilidade e governanca para alimentar casos de uso de BI, analises ad-hoc e aprendizado de maquina.

## 1. Camada Bronze (Dados Brutos / Ingestao)

A camada bronze e o ponto de entrada de todos os dados no lakehouse. 
- Caracteristicas principais:
  - Mantem o estado bruto original dos sistemas de origem (append-only).
  - Preserva metadados de ingestao como timestamp de carregamento, nome do arquivo de origem e esquema original.
  - Aceita dados estruturados, semi-estruturados (JSON, XML) e nao estruturados.
  - Nenhum filtro ou transformacao de negocio e aplicado nesta etapa para permitir auditoria e reprocessamento historico completo.
- Tecnologias recomendadas: Databricks Auto Loader (`cloudFiles`) para ingestao incremental e escalavel de arquivos em nuvem (S3, ADLS, GCS).

## 2. Camada Silver (Dados Limpos e Enriquecidos)

A camada silver representa a visao corporativa integrada e consistente dos dados.
- Caracteristicas principais:
  - Limpeza, validacao de tipos e padronizacao de formatos de datas e strings.
  - Deduplicacao e resolucao de registros inconsistentes (usando comandos Delta `MERGE INTO`).
  - Enriquecimento atraves de juncoes com tabelas de referencia e dimensoes estaticas.
  - Aplicacao de esquemas estruturados e verificacao de regras de qualidade de dados.
- Casos de uso: Consultas de analistas de dados, servicos operacionais e preparacao de features para machine learning.

## 3. Camada Gold (Agregacoes de Negocio e Modelagem Analitica)

A camada gold contem dados organizados especificamente para atender objetivos de negocio e relatorios finais.
- Caracteristicas principais:
  - Modelagem dimensional (Star Schema / Fato e Dimensoes) ou data marts agregados por periodos (diario, mensal).
  - Regras de negocio complexas e metricas consolidadas (ex: churn, faturamento consolidado, tempo medio de resposta).
  - Otimizada para consultas analiticas de alta performance com leitura em larga escala.
- Casos de uso: Dashboards executivos em ferramentas de BI (Power BI, Tableau, Databricks SQL), relatorios financeiros e analises regulatórias.
