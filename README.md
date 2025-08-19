# SPTrans Olho Vivo Data Pipeline

## Introduction
This pipeline was developed to collect, process, and provide real-time public transport data for the city of São Paulo. Its main focus is to transform raw data from the SPTrans Olho Vivo API into information ready for analysis, supporting decision-making in urban mobility.

## Objective
The objectives of this pipeline are to:
- Automate the collection of real-time bus data.
- Ensure reliable and durable data storage.
- Apply transformations for data cleaning and standardization.
- Provide data ready for analysis and visualization in Power BI dashboards.

## Data Source: SPTrans Olho Vivo API
- **Description:** The Olho Vivo API provides real-time information on the location, routes, and itineraries of São Paulo municipal buses.
- **Format:** JSON
- **Key information provided:**
  - Vehicle and line identification
  - Location (latitude and longitude)
  - Lines, origins, and destinations
  - Timestamp of the last update
- **Frequency:** Data is continuously updated by the API and consumed by the pipeline every 10 minutes.
- **Authentication:** The API requires an access key (token), which must be configured in the collection script.
- **Link:** [SPTrans Developers](https://www.sptrans.com.br/desenvolvedores/)

## Architecture

1. **Data Collection**
   - **Source:** SPTrans Olho Vivo API
   - **Technology:** Python
   - **Description:** Real-time public transport data is periodically consumed via HTTP requests (e.g., every 30 seconds).

2. **Transmission and Temporary Storage**
   - **Technology:** Kafka + NiFi + MinIO
   - **Description:**
     - Data is sent to Kafka topics.
     - NiFi consumes data from Kafka and writes files to MinIO (JSON format), ensuring durability.
     - Ingestion logs are recorded to monitor processing and failures.

3. **Processing and Transformation**
   - **Technology:** PySpark (Jupyter Notebook)
   - **Description:**
     - Reads files from MinIO.
     - Transformations: cleaning, field standardization, timestamp handling, and partial aggregations.
     - Ingestion logs are recorded to monitor processing and failures.

4. **Layered Storage (Medallion Architecture)**
   - **Technology:** PostgreSQL
   - **Layers:**
     - **Bronze:** Raw data as received from the API.
     - **Silver:** Cleaned data with proper data types.
     - **Gold:** Standardized technical names to business-friendly names and calculated fields.

5. **Visualization**
   - **Technology:** Power BI
   - **Description:** Dashboards for monitoring buses, delays, and the busiest lines in São Paulo.
