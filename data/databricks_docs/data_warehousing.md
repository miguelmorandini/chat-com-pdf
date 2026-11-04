# Data Warehouses e SQL Warehouses no Databricks

No contexto de dados e no ecossistema Databricks, o termo "warehouse" pode se referir tanto ao conceito arquitetural classico de **Data Warehouse** quanto ao recurso de computacao **SQL Warehouse** do Databricks.

## 1. O que e um Data Warehouse (Conceito Tradicional)

Um **Data Warehouse** (Armazem de Dados) e um repositorio centralizado projetado especificamente para analises de negocios, relatorios operacionais e Business Intelligence (BI).
- **Caracteristicas principais:**
  - Armazena dados estruturados e limpos, organizados frequentemente em esquemas estrela (Star Schema) com tabelas de Fatos e Dimensoes.
  - Otimizado para consultas analiticas complexas (OLAP) e leitura em massa.
  - Oferece suporte nativo a transacoes ACID e controle rigoroso de esquema (Schema-on-Write).
- **Limitacoes classicas:** Dificuldade para lidar com dados semi-estruturados (JSON, logs) e nao-estruturados (imagens, audio, video), custo elevado de armazenamento proprietario e falta de suporte nativo para fluxos de Machine Learning e processamento em tempo real (streaming).
- **Como o Lakehouse se relaciona:** A arquitetura Lakehouse do Databricks combina o melhor dos dois mundos: a flexibilidade e baixo custo de armazenamento do Data Lake com a confiabilidade, governanca e desempenho SQL de um Data Warehouse.

## 2. O que e um SQL Warehouse no Databricks

No Databricks, um **SQL Warehouse** e um recurso de computacao especializado, otimizado para executar consultas analiticas em SQL, carregar dashboards do Databricks SQL e atender ferramentas externas de BI (como Power BI, Tableau e DBeaver).

- **Como funciona:**
  - Em vez de usar um cluster tradicional de computacao de engenharia, o usuario conecta seu dashboard ou editor SQL a um SQL Warehouse.
  - Ele utiliza o motor vetorizado nativo **Photon** em C++ para processamento ultrarrapido de queries SQL.
- **Tipos de SQL Warehouse:**
  1. **Serverless SQL Warehouse:** Provisionamento instantaneo em segundos na nuvem gerenciada pela Databricks, com escalabilidade automatica e desligamento automatico por inatividade para reducao de custos.
  2. **Pro / Classic SQL Warehouse:** Roda na conta de nuvem do cliente com controle tradicional de instancias.
- **Auto-stop e Escalabilidade:** Suporta auto-scaling de clusters para lidar com picos de concorrencia de analistas de negocio sem travamento de filas.
