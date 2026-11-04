# Governanca Centralizada com Unity Catalog no Databricks

O Unity Catalog e a solucao de governanca unificada do Databricks para gerenciar dados e ativos de inteligencia artificial (modelos, funcoes, volumes e arquivos) em multiplos workspaces e nuvens (AWS, Azure e GCP).

## 1. O Namespace de Tres Niveis

O Unity Catalog introduz uma hierarquia formal de tres niveis para organizacao e referenciamento de tabelas e views:
`catalog.schema.table`

- **Catalog (Catalogo):** O nivel mais alto de isolamento organizacional. Tipicamente corresponde a um ambiente (ex: `dev`, `staging`, `prod`) ou a uma unidade de negocio (ex: `financeiro`, `marketing`, `logistica`).
- **Schema / Database (Esquema):** O segundo nivel, utilizado para agrupar tabelas semanticamente relacionadas dentro de um catalogo (ex: `vendas`, `crm`, `faturamento`).
- **Table / View / Volume (Ativo):** O objeto de dados em si (ex: `pedidos`, `clientes`).

Beneficios em relacao ao modelo antigo (Hive Metastore):
- Elimina a necessidade de prefixos artificiais em nomes de tabelas.
- Permite replicar e migrar codigo entre ambientes apenas alterando o catalogo de contexto (`USE CATALOG prod`).
- Isolamento claro de permissoes em qualquer nivel da hierarquia (conceder permissao em um catalogo herda para todos os esquemas e tabelas filhos).

## 2. Controle de Acesso e Seguranca Granular

O Unity Catalog adota padroes ANSI SQL para controle de privilegios:
```sql
GRANT SELECT ON TABLE prod.vendas.pedidos TO `analistas_financeiros`;
GRANT USE CATALOG ON CATALOG prod TO `engenharia_dados`;
```

Recursos avancados de seguranca:
- **Mascaramento de Colunas (Column Masking):** Permite ofuscar colunas sensiveis (ex: CPF, cartao de credito) dependendo do grupo do usuario executando a consulta:
  ```sql
  CREATE OR REPLACE FUNCTION mascara_cpf(cpf STRING)
  RETURN CASE WHEN is_account_group_member('rh') THEN cpf ELSE '***.***.***-**' END;
  ```
- **Filtro de Linhas (Row-Level Security):** Restringe as linhas retornadas com base na regiao ou permissao do usuario logado.

## 3. Linhagem Automatica de Dados (Data Lineage)

O Unity Catalog captura automaticamente a linhagem de ponta a ponta em tempo de execucao, cobrindo:
- De qual tabela origem cada tabela ou coluna foi derivada (linhagem ao nivel de coluna).
- Quais notebooks, jobs, pipelines Delta Live Tables e dashboards consumiram ou geraram os dados.
- Rastreamento de modelos de ML e datasets de treinamento.
A linhagem nao exige configuracao manual nem instrumentacao de codigo: ela e inferida pelo compilador do Spark.
