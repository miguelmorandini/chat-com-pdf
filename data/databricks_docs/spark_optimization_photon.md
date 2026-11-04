# Otimizacao de Performance no Databricks: Photon e Spark

O processamento eficiente no Databricks combina o poder distribuido do Apache Spark com o motor vetorizado nativo Photon desenvolvido pela Databricks.

## 1. O Motor Vetorizado Photon

O Photon e um motor de execucao nativo reescrito do zero em C++ para maximizar o aproveitamento da arquitetura de hardware moderno (instrucoes SIMD da CPU, paralelismo de registradores e hierarquia de memoria cache L1/L2/L3).
- **Substituicao transparente:** O Photon substitui o executor tradicional baseado na JVM em operacoes SQL e DataFrame (agregacoes, joins, filtros e gravacoes Parquet/Delta).
- **Beneficios:** Acelera em ate 3x a 5x consultas analiticas e processamento em lote sem necessidade de alterar o codigo SQL ou Python existente.

## 2. Adaptive Query Execution (AQE)

O Adaptive Query Execution e um recurso do Spark que reotimiza o plano de consulta durante o tempo de execucao com base em estatisticas reais intermediarias:
- **Conversao Dinamica para Broadcast Join:** Se apos a aplicacao de filtros uma tabela grande diminuir de tamanho e ficar menor que o limite de broadcast (padrao 10MB), o AQE altera o plano em tempo de execucao de Sort Merge Join para Broadcast Hash Join, eliminando o shuffle de rede.
- **Coalescencia Dinamica de Particoes de Shuffle:** Reduz automaticamente o numero excessivo de particoes pequenas geradas por operacoes de shuffle (como GROUP BY), evitando sobrecarga de tarefas minusculas na JVM.
- **Tratamento de Skew Join (Desbalanceamento de Dados):** Detecta particoes desproporcionalmente grandes (assimetria) causadas por chaves de join frequentes (ex: 'NULL' ou 'NA') e as subdivide em sub-tarefas paralelas, evitando que um unico executor trave a conclusao do job.

## 3. Estrategias de Join e Boas Praticas

- **Broadcast Hash Join (BHJ):** A tabela menor e transmitida integralmente para todos os executores. Elimina totalmente a fase cara de Shuffle (troca de dados via rede).
  ```python
  from pyspark.sql.functions import broadcast
  df_final = df_vendas.join(broadcast(df_categorias), "id_categoria")
  ```
- **Sort Merge Join (SMJ):** Utilizado para duas tabelas grandes. Exige ordenar e redistribuir os dados por chave em toda a rede.
- **Liquid Clustering (substituto moderno do particionamento tradicional):** Recomendado pelo Databricks para novas tabelas em substituicao ao particionamento por diretorios físicos (`PARTITIONED BY (data)`). O Liquid Clustering suporta alteracao flexivel de chaves de agrupamento sem reconstruir a tabela inteira e evita o problema comum de particoes excessivamente pequenas.
