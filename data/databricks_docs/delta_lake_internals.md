# Funcionamento Interno e Transacoes ACID no Delta Lake

O Delta Lake e uma camada de armazenamento open-source que adiciona confiabilidade, desempenho e governanca sobre data lakes em nuvem (Amazon S3, Azure Data Lake Storage, Google Cloud Storage), armazenando os dados em formato Apache Parquet e utilizando um log transacional proprietario.

## 1. O Log Transacional (_delta_log)

O nucleo do Delta Lake e o log de transacoes, mantido no diretorio `_delta_log/` no caminho raiz de cada tabela Delta.
- Cada operacao que modifica a tabela (INSERT, UPDATE, DELETE, MERGE) gera um novo arquivo commit no formato JSON: `00000000000000000000.json`, `00000000000000000001.json`, etc.
- O arquivo de commit contem acoes atomicas:
  - `add`: Caminho de um novo arquivo Parquet gerado com novos dados.
  - `remove`: Marcacao logica de um arquivo Parquet que nao deve mais ser considerado ativo na versao atual (sem excluir o arquivo fisicamente no momento da gravacao).
  - `metaData`: Definicao do esquema da tabela e configuracoes.
  - `commitInfo`: Autor, operacao e timestamp da transacao.

## 2. Checkpoints em Apache Parquet

A cada 10 commits, o Delta Lake consolida automaticamente o historico dos commits JSON anteriores em um unico arquivo de checkpoint no formato Parquet (ex: `00000000000000000010.checkpoint.parquet`).
Isso evita que o driver precise ler milhares de arquivos JSON para reconstruir o estado atual da tabela, permitindo listar particoes e arquivos validos instantaneamente.

## 3. Concorrencia Otimista (Optimistic Concurrency Control - OCC)

O Delta Lake utiliza controle de concorrencia otimista para coordenar gravacoes simultaneas:
1. O leitor/gravador registra a versao inicial da tabela no momento em que inicia.
2. Escreve os novos arquivos Parquet em segundo plano.
3. Tenta commitar o arquivo JSON da proxima versao. Se outra transacao tiver commitado a mesma versao antes, o Delta Lake verifica se houve conflito logico (modificacao nos mesmos arquivos ou particoes). Se nao houver conflito, o Delta faz retry automatico; se houver, a transacao falha de forma segura sem corromper os dados.

## 4. Time Travel (Viagem no Tempo)

Como os arquivos removidos sao marcados apenas logicamente no log, o Delta Lake permite consultar versoes anteriores da tabela:
- Por versao: `SELECT * FROM tabela VERSION AS OF 5`
- Por timestamp: `SELECT * FROM tabela TIMESTAMP AS OF '2026-11-01 10:00:00'`
Isso permite reproduzir auditorias, reverter atualizacoes incorretas e treinar modelos de ML com snapshots confiaveis de dados historicos.

## 5. Otimizacao de Arquivos: OPTIMIZE, Z-ORDER e Liquid Clustering

- `OPTIMIZE`: Compacta milhares de pequenos arquivos Parquet em arquivos maiores de tamanho ideal (tipicamente 1GB) para acelerar a leitura e reduzir chamadas a API do storage.
- `Z-ORDER BY (col1, col2)`: Algoritmo de curva multidimensional de preenchimento de espaco que agrupa valores correlacionados nos mesmos arquivos Parquet, permitindo o pulo eficiente de dados (data skipping) ao filtrar por multiplas colunas.
- `Liquid Clustering`: O padrao moderno do Databricks que substitui o particionamento tradicional e o Z-Order por agrupamento incremental dinamico sem necessidade de reescrever particoes inteiras.
