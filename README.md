# Welcome Gaiz DF 10

## Let's have func

### Day 1:
- Data Lake (GCS)
    - What is a Data Lake
    - ELT vs. ETL
    - What is an Orchestration Pipeline? 
    - What is a DAG?
    - Setting up Airflow locally
    - Setting up Airflow with Docker-Compose

### Day 2:
- Ingesting Data to GCP with Airflow
    - Extraction: Download and unpack the data
    - Pre-processing: Convert this raw data to parquet
    - Upload the parquet files to GCS
    - Create an external table in BigQuery
    - Converting the ingestion script for loading data to Postgres to Airflow DAG
    - OLAP vs OLTP

### Day 3:
- Data Warehouse
    - What is data warehouse
    - Intro to BigQuery.
    - Loading Data into BigQuery.
    - Exploring Schemas.
    - Schema Design.
    - Nested and Repeated Fields.
    - Partitioning and Clustering.

### Day 4:
- Analytics Engineering
    - ETL vs ELT
    - Data modeling concepts (fact and dim tables)
    - Intro to DBT
    - Development of dbt models
    - Anatomy of a dbt model: written code vs compiled Sources
    - Materialisations: table, view, incremental, ephemeral
    - Jinja and Macros, Packages, Variables, Tests, Documentation
    - Gathering and documenting business requirements