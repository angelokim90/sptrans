# Pipeline de Dados - SPTrans Olho Vivo

## Introdução
Esta pipeline foi desenvolvida para coletar, processar e disponibilizar dados de transporte público em tempo real da cidade de São Paulo. O foco é transformar dados brutos da API SPTrans Olho Vivo em informações prontas para análise, apoiando a tomada de decisão em mobilidade urbana.

## Objetivo
O objetivo desta pipeline é:
- Automatizar a coleta de dados de ônibus em tempo real.
- Garantir armazenamento confiável e durável dos dados.
- Aplicar transformações para limpeza e padronização.
- Disponibilizar dados prontos para análise e visualização em dashboards no Power BI.

## Fonte de Dados: API SPTrans Olho Vivo
- **Descrição:** A API Olho Vivo fornece informações em tempo real sobre localização, linhas e itinerários de ônibus municipais de São Paulo.
- **Formato:** JSON
- **Principais informações fornecidas:**
  - Identificação do veículo e linha
  - Localização (latitude e longitude)
  - Linhas, origens e destinos
  - Horário da última atualização
- **Periodicidade:** Dados atualizados constantemente pela API, consumidos pela pipeline a cada 10 minutos.  
- **Autenticação:** A API requer chave de acesso (token), que deve ser configurada no script de coleta.
- **Link:** https://www.sptrans.com.br/desenvolvedores/

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

