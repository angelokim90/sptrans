# sptrans
Pipeline: api sptrans olho vivo, kafka,nifi, minio, pyspark, postgres, power bi


**Arquitetura**
**1. Coleta de Dados**

Fonte: API SPTrans Olho Vivo

Tecnologia: Python

Descrição: Dados de transporte público em tempo real são consumidos periodicamente via requisições HTTP à API.

**2. Transmissão e Armazenamento Temporário**

Tecnologia: Kafka + NiFi + MinIO

Descrição:

Os dados recebidos da API são enviados para tópicos Kafka.

NiFi consome os dados do Kafka e armazena arquivos no MinIO, garantindo persistência e durabilidade.

**3. Processamento e Transformação**

Tecnologia: PySpark (Jupyter Notebook)

Descrição:

Os arquivos armazenados no MinIO são lidos via PySpark.

Aplicam-se transformações e limpeza dos dados antes da carga no banco.

**4. Armazenamento em Camadas (Medalhão)**

Tecnologia: PostgreSQL

Descrição:

Bronze: Dados crus, exatamente como foram recebidos da API.

Silver: Dados limpos e padronizados.

Gold: Dados agregados e prontos para análise.

**5. Visualização**

Tecnologia: Power BI

Descrição: Os dados na camada Gold são consumidos para gerar dashboards de monitoramento e análise de transporte público em São Paulo.

