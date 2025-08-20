# SPTrans Olho Vivo Data Pipeline

## Introduction
This pipeline was developed to collect, process, and provide real-time public transport data for the city of São Paulo. Its main focus is to transform raw data from the SPTrans Olho Vivo API into information ready for analysis, supporting decision-making in urban mobility.

## Objective
The objectives of this pipeline are to:
- Automate the collection of real-time bus data.
- Ensure reliable and durable data storage.
- Apply transformations for data cleaning and standardization.
- Provide data ready for analysis and visualization in Power BI dashboards.

## Data Environment Note
All software used in this pipeline (Python, Kafka, NiFi, MinIO, PostgreSQL, PySpark) was run via Docker, ensuring portability, consistency, and ease of environment versioning.
Power BI was used outside of Docker due to the need for version control and dashboard management, which depend on the Windows/GUI environment.

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

## Educational Exceptions
- **Trusted layer**: stored in Parquet and flat files *for educational purposes only and for easier readability*.
- **Bronze layer**: stored in PostgreSQL *solely for didactic visualization purposes*.

## Architecture

1. **Data Collection**
   - **Source:** SPTrans Olho Vivo API
   - **Technology:** Python
   - **Description:** Real-time public transport data is periodically consumed via HTTP requests (e.g., every 30 seconds).

2. **Transmission and Storage**
   - **Technology:** Kafka + NiFi + MinIO
   - **Description:**
     - Data is sent to Kafka topics.
     - NiFi consumes data from Kafka and writes files to MinIO (JSON format), ensuring durability.
     - Ingestion logs are recorded to monitor processing and failures.
  
   - **Consuming data with Kafka:** <img width="854" height="727" alt="image" src="https://github.com/user-attachments/assets/dc4b4728-fd5a-4765-a34e-bf1e9a7935e8" />
   - **Nifi Pipeline:** <img width="1357" height="861" alt="image" src="https://github.com/user-attachments/assets/afe5effb-9583-4df3-9e0b-fb88deee1793" />
   - **Minio Raw Stage:** <img width="1909" height="575" alt="image" src="https://github.com/user-attachments/assets/c9f5954f-b372-4fd9-9b36-608729566cb8" />

3. **Processing and Transformation**
   - **Technology:** PySpark (Jupyter Notebook)
   - **Description:**
     - Reads files from MinIO.
     - Transformations: cleaning, field standardization, timestamp handling.
     - Ingestion logs are recorded to monitor processing and failures.

4. **Service Storage (Medallion Architecture)**
   - **Technology:** PostgreSQL
   - **Layers:**
     - **Bronze:** Raw data as received from the API.
     - **Silver:** Cleaned data with proper data types.
     - **Gold:** Standardized technical names to business-friendly names and calculated fields.
   - Postgre Schemas:
   <img width="354" height="413" alt="image" src="https://github.com/user-attachments/assets/a7f1b3d7-6a13-4762-ba97-a8e03d5ef605" />

5. **Visualization**
   - **Technology:** Power BI
   - **Description:** Dashboards for monitoring buses, delays, and the busiest lines in São Paulo.

6. **Data Architecture**
   - **Diagram:**
     
![pipeline (2)](https://github.com/user-attachments/assets/c89b1be0-bdd0-4d29-8fca-98f15c5bd816)

## Dashboard Power BI
- **Dashboard:**
<img width="1433" height="807" alt="image" src="https://github.com/user-attachments/assets/cf536b08-73e3-45a1-a6ac-c2843e2ef995" />


- **Link:** [PowerBI_SPTRANS](https://app.powerbi.com/view?r=eyJrIjoiOWIxZDAwNjAtOTdhZS00ZDg3LThlNDMtNTFmMTcxY2ZmNGRjIiwidCI6ImY4ODc5ODgyLTNkM2ItNDg2Zi05OTA0LTc0Zjc4YTBlZGQ1MCJ9)

## Conclusion

- **Conclusion:**
This SPTrans Olho Vivo Data Pipeline demonstrates a robust approach to collecting, processing, and delivering real-time public transport data for São Paulo. By leveraging a combination of Dockerized services, Kafka streaming, NiFi ingestion, MinIO storage, PySpark processing, and PostgreSQL medallion architecture, the pipeline ensures data reliability, scalability, and readiness for analysis. The integration with Power BI allows city planners, analysts, and decision-makers to visualize key metrics, monitor bus operations, and make informed decisions to improve urban mobility. Additionally, the inclusion of educational exceptions highlights best practices in data management while maintaining clarity and accessibility for learning purposes.
