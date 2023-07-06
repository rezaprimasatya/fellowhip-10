# ELT and ETL

- ELT (Extract, Load, Transform): 
    - In ELT, the data is first extracted from the source system and loaded into a data warehouse. Only after it is in the warehouse is the data transformed. This is possible due to the high processing power of modern data warehouses like BigQuery. The transformations happen in SQL or another data manipulation language.

- ETL (Extract, Transform, Load): 
    - ETL is a data integration process that involves extracting data from source systems, transforming it in a staging area, and then loading the transformed data into a data warehouse. The transformation process involves cleansing, denormalizing, and aggregating the data so it can be used for business reporting.

### Shifting Paradigm from ETL to ELT
The shift from ETL to ELT is driven by the explosion of data volume and the increasing power of cloud-based data warehouses like BigQuery. In ELT, you can leverage the full power of the data warehouse to process transformations, which is typically much more scalable and faster. This is in contrast to ETL, where the transformations are processed in an external tool, which can be a bottleneck.

### ETL vs ELT Differences

|                 | ETL                                             | ELT                                                |
|-----------------|-------------------------------------------------|----------------------------------------------------|
| Data processing | Processed before loading into warehouse         | Loaded into the warehouse before processing        |
| Performance     | Limited by ETL tool capacity                    | Can leverage full power of the warehouse           |
| Complexity      | Complex transformations must be defined upfront | Can iteratively develop and refine transformations |
| Data Storage    | Only transformed data is stored                 | Both raw and transformed data are stored           |

### ETL Process
- Extract: Get data from various source systems
- Transform: Clean, normalize, and transform the data in a staging area
- Load: Load the transformed data into a data warehouse

```sh
# Python code for a simple ETL process
import pandas as pd
from sqlalchemy import create_engine

# Extract
data = pd.read_csv('source_data.csv')

# Transform
data['new_column'] = data['column1'] + data['column2']

# Load
engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')
data.to_sql('table_name', engine)
```

### ELT Process
- Extract: Get data from various source systems
- Load: Load the raw data into a data warehouse
- Transform: Transform the data using the warehouse's processing power

```sh
# Python code for a simple ELT process
import pandas as pd
from sqlalchemy import create_engine

# Extract
data = pd.read_csv('source_data.csv')

# Load
engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')
data.to_sql('raw_table', engine)

# Transform
with engine.connect() as conn:
    conn.execute("""
        INSERT INTO transformed_table 
        SELECT column1, column1 + column2 as new_column
        FROM raw_table
    """)
```

### ETL vs ELT Similarities
|         | ETL                                                                         | ELT                                                                         |
|---------|-----------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| Extract | Data is extracted from source systems in both processes                     | Data is extracted from source systems in both processes                     |
| Load    | Data is loaded into the warehouse in both processes                         |                                                                             |
| Goal    | Both aim to transform and store data for analysis and business intelligence | Both aim to transform and store data for analysis and business intelligence |

### ODS, CDM, ADS layers
- Operational Data Store (ODS): This is a database designed to integrate data from multiple sources for additional operations on the data. This is a place where most businesses will place a copy of their operational data.

```sh
# Python code to load data into ODS
# Assume data1, data2 are dataframes containing data from different sources
ods_data = pd.concat([data1, data2])
ods_data.to_sql('ods_table', engine)
```

- Common Data Model (CDM): This represents a logical definition of your standardized, cleansed data structures. Here, data is transformed, cleaned, and loaded from ODS to give a unified view.

```sh
# Python code to create CDM from ODS
with engine.connect() as conn:
    conn.execute("""
        INSERT INTO cdm_table 
        SELECT column1, column2, AVG(column3) OVER (PARTITION BY column1)
        FROM ods_table
    """)
```

- Application Data Store (ADS): This is a database which holds the final processed and aggregated data which is ready for access and used by end-user tools such as reporting tools, dashboards, etc.
```sh
# Python code to create ADS from CDM
with engine.connect() as conn:
    conn.execute("""
        INSERT INTO ads_table 
        SELECT column1, SUM(column2)
        FROM cdm_table
        GROUP BY column1
    """)
```

# ETL/ELT in GCP

### ETL with BigQuery, DBT, Cloud Composer, Cloud Storage, and Cloud Dataflow
In an ETL process:

- Cloud Storage: Data is first stored here after being extracted from the source systems.
- Cloud Dataflow: You then use Dataflow to process and transform the data. This could involve cleaning, aggregating, and joining data.
- BigQuery: The transformed data is loaded into BigQuery for further analysis.
- Cloud Composer: This tool is used to orchestrate the ETL process. It can schedule and manage workflows that consist of multiple tasks, like starting a Dataflow job, running a BigQuery query, etc.

The below Python code uses Apache Beam (which is what Dataflow is based on) to read a CSV file from Cloud Storage, transform the data, and write it to BigQuery.

```sh
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToBigQuery

options = PipelineOptions(flags=[], project='my-project-id')

p = beam.Pipeline(options=options)

def transform_data(element):
    # Add your transformation logic here
    return element

data = (
    p
    | 'Read from Cloud Storage' >> ReadFromText('gs://my-bucket/my-file.csv')
    | 'Transform data' >> beam.Map(transform_data)
    | 'Write to BigQuery' >> WriteToBigQuery(
        table='my_table',
        dataset='my_dataset',
        project='my-project-id',
        schema='column1:STRING,column2:INTEGER',
    )
)

p.run().wait_until_finish()
```

### ELT with BigQuery, DBT, Cloud Composer, Cloud Storage, and Cloud Dataflow
- Cloud Storage: Data is first stored here after being extracted from the source systems.
- BigQuery: The raw data is immediately loaded into BigQuery.
- DBT: This tool is used to transform the data. It allows you to write transformations as SQL queries and manages the execution of these transformations.
- Cloud Composer: This tool is used to orchestrate the ELT process. It can schedule and manage workflows that consist of loading data to BigQuery, running DBT transformations, etc.

The below Python code uses the google-cloud-bigquery library to load a CSV file from Cloud Storage to BigQuery.

```sh
from google.cloud import bigquery

client = bigquery.Client()

uri = 'gs://my-bucket/my-file.csv'
table_id = 'my-project-id.my_dataset.my_table'

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=True,
)

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)

load_job.result()  # Wait for the job to complete.

table = client.get_table(table_id)  # Get table details
print(f'Loaded {table.num_rows} rows to {table_id}.')
```

Then you can use DBT to transform the data. You would write a SQL file like this:
```sh
-- my_transformation.sql
SELECT column1, column2, AVG(column3) OVER (PARTITION BY column1) as avg_column3
FROM `my-project-id.my_dataset.my_table`
```

And a DBT model file like this:
```sh
# dbt```yaml
# dbt_project.yml
name: 'my_dbt_project'
version: '1.0.0'
profile: 'default'

models:
  my_dbt_project:
    # Apply to all models within this project.
    materialized: 'table'

    my_transformation:
      materialized: 'table'
      sql: '{% include "my_transformation.sql" %}'
```

Then, you would run DBT to execute the transformation:
```sh
dbt run --model my_transformation
```

You would use Cloud Composer to orchestrate these tasks. This involves writing a DAG (Directed Acyclic Graph) using Apache Airflow, which Cloud Composer is based on. However, writing an Airflow DAG is beyond the scope of this response.

# Use Cases in Banking
- ETL Example: A bank may use an ETL process to prepare data for regulatory reporting. The raw data from various systems is extracted, transformed to meet the specific requirements of the regulatory reports, and loaded into a data warehouse. From there, the reports are generated and sent to the regulators. 
- Tools like Informatica, Datastage, or even Cloud-based ETL tools like Google's DataFlow could be used.

- ELT Example: For internal reporting and analysis, a bank may use an ELT process. Here, raw data from various systems is loaded into a data warehouse like BigQuery. Then, analysts and data scientists can use SQL and other tools to create their own transformations and analyses. 
- Tools involved could be Google Cloud Storage for storing raw data, BigQuery for the data warehouse, and DBT for transformations.

Challenges in both cases could involve data security and privacy, data quality, and data integration from various systems. The techniques and tools mentioned above can help address these issues, along with good data governance practices.