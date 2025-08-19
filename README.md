# Pipeline de Dados - SPTrans Olho Vivo

Esta pipeline coleta, processa e disponibiliza dados da API SPTrans Olho Vivo para análise em Power BI, utilizando tecnologias de streaming, processamento distribuído e banco de dados em camadas.

## Arquitetura

1. **Coleta de Dados**
   - **Fonte:** API SPTrans Olho Vivo
   - **Tecnologia:** Python
   - **Descrição:** Dados de transporte público em tempo real são consumidos periodicamente via requisições HTTP (ex.: a cada 30 segundos).

2. **Transmissão e Armazenamento Temporário**
   - **Tecnologia:** Kafka + NiFi + MinIO
   - **Descrição:**
     - Dados enviados para tópicos Kafka.
     - NiFi consome dados do Kafka e grava arquivos no MinIO (formato JSON), garantindo durabilidade.
     - Logs de ingestão são registrados para monitoramento de processamento e falhas.

3. **Processamento e Transformação**
   - **Tecnologia:** PySpark (Jupyter Notebook)
   - **Descrição:**
     - Leitura de arquivos do MinIO.
     - Transformações: limpeza, padronização de campos, tratamento de timestamps e agregações parciais.
     - Logs de ingestão são registrados para monitoramento de processamento e falhas.

4. **Armazenamento em Camadas (Medalhão)**
   - **Tecnologia:** PostgreSQL
   - **Camadas:**
     - **Bronze:** Dados crus, como recebidos da API.
     - **Silver:** Dados limpos e tipagem de dados.
     - **Gold:** Padronização dos nomes técnicos para business name e campos calculados.

5. **Visualização**
   - **Tecnologia:** Power BI
   - **Descrição:** Dashboards para monitoramento de veículos, atrasos e linhas mais movimentadas em São Paulo.

