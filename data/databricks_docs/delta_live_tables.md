# Pipelines Declarativos com Delta Live Tables (DLT)

Delta Live Tables (DLT) e um framework declarativo do Databricks para construir pipelines de processamento de dados confiaveis, testaveis e de facil manutencao, utilizando Python ou SQL.

## 1. Abordagem Declarativa vs Imperativa

Em vez de escrever codigo imperativo gerenciando checkpoints de streaming, criacao de tabelas intermediarias e tratamento de falhas em clusters manuais, o engenheiro declara apenas o que deseja transformar:
- O DLT gerencia a infraestrutura, execucao em grafo direcionado aciclico (DAG), escalabilidade de cluster e recuperacao de falhas automaticamente.

## 2. Tipos de Tabelas no DLT

- **Streaming Tables:** Tabelas alimentadas por fontes contínuas ou de mudanca constante (ex: Auto Loader lendo arquivos novos de um bucket). Processa apenas registros novos (apenas append) com custo computacional minimo.
- **Materialized Views:** Tabelas calculadas com base em uma consulta SQL que agrega ou transforma dados. O DLT atualiza os resultados de forma eficiente conforme os dados subjacentes mudam.

Exemplo de declaracao em Python:
```python
import dlt
from pyspark.sql.functions import *

@dlt.table(
    comment="Tabela Bronze ingerida de arquivos brutos"
)
def pedidos_bronze():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("/mnt/raw/pedidos/")
    )
```

## 3. Gestao de Qualidade de Dados com Expectations

O DLT possui tratamento nativo de qualidade atraves de regras de validacao chamadas Expectations:
- **`@dlt.expect("regra", "condicao")`:** Registra metricas de violacao no log e mantem o registro na tabela (alerta informativo).
- **`@dlt.expect_or_drop("regra", "condicao")`:** Descarta o registro que violar a condicao, mantendo apenas dados validos na tabela final.
- **`@dlt.expect_or_fail("regra", "condicao")`:** Interrompe a execucao do pipeline imediatamente se qualquer registro violar a regra critica (ex: chave primaria nula).

Exemplo:
```python
@dlt.table
@dlt.expect_or_drop("preco_positivo", "valor_unitario > 0")
@dlt.expect_or_fail("id_obrigatorio", "id_pedido IS NOT NULL")
def pedidos_silver():
    return dlt.read_stream("pedidos_bronze")
```
Todas as metricas de quantas linhas passaram e quantas foram descartadas sao automaticamente expostas no catalogo e nos logs de auditoria.
