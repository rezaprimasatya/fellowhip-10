### Batch Loading Data from Cloud Storage:
Batch loading involves loading data in bulk from Cloud Storage into BigQuery. It is suitable for scenarios where data is periodically updated or when working with large datasets.

- Use Case: Analyzing historical sales data from a retail company to identify trends and patterns.

            +-------------------+
            |    Cloud Storage  |
            +-------------------+
                      |
                      |
          +-----------+-----------+
          |                       |
          |    BigQuery           |
          |                       |
          +-----------------------+
- Technique: BigQuery provides various techniques to optimize data loading, such as batch loading from multiple files, using partitioned tables, and leveraging data formats like Avro, Parquet, or ORC for efficient storage.

```sh
from google.cloud import bigquery

def load_data_from_gcs():
    client = bigquery.Client()
    dataset_id = 'your_dataset_id'
    table_id = 'your_table_id'
    uri = 'gs://your_bucket/data.csv'

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField('column1', 'STRING'),
            bigquery.SchemaField('column2', 'INTEGER'),
            # Add more schema fields as necessary
        ],
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
    )

    load_job = client.load_table_from_uri(uri, dataset_id + '.' + table_id, job_config=job_config)
    load_job.result()  # Waits for the job to complete

    table = client.get_table(dataset_id + '.' + table_id)
    print('Loaded {} rows into {}:{}.'.format(table.num_rows, dataset_id, table_id))
```

```sh
CREATE TABLE your_dataset.your_table
(
    column1 STRING,
    column2 INTEGER,
    -- Add more columns as necessary
);

LOAD your_dataset.your_table
FROM 'gs://your_bucket/data.csv'
OPTIONS(
    skip_leading_rows=1,
    format='CSV'
);
```


### Batch Loading Data from Cloud SQL MySQL:

Batch loading data from Cloud SQL MySQL involves extracting data from a MySQL database hosted on Cloud SQL and loading it into BigQuery. It is useful for scenarios where data is stored in a relational database and needs to be analyzed in BigQuery.

- Use Case: Analyzing customer behavior data stored in a Cloud SQL MySQL database to gain insights into user preferences.

        +-------------------+
        |    Cloud SQL      |
        |    (MySQL)        |
        +-------------------+
                  |
                  |
      +-----------+-----------+
      |                       |
      |    BigQuery           |
      |                       |
      +-----------------------+
- Technique: The Cloud SQL federated query feature allows querying data directly from Cloud SQL MySQL in BigQuery without the need to load the data into BigQuery storage.

```sh
from google.cloud import bigquery

def load_data_from_cloudsql():
    client = bigquery.Client()
    dataset_id = 'your_dataset_id'
    table_id = 'your_table_id'
    project_id = 'your_project_id'
    connection_name = 'your_connection_name'
    database_name = 'your_database_name'
    username = 'your_username'
    password = 'your_password'

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField('column1', 'STRING'),
            bigquery.SchemaField('column2', 'INTEGER'),
            # Add more schema fields as necessary
        ],
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    table_ref = client.dataset(dataset_id).table(table_id)
    load_job = client.load_table_from_uri(
        'bigquery://{}.{}/{}'.format(project_id, dataset_id, table_id),
        table_ref,
        job_config=job_config,
        location='us',
        project_id=project_id,
        connection=connection_name,
        source='connection://{}/{}'.format(database_name, username),
        labels={'name': 'load_data_from_cloudsql'}
    )

    load_job.result()  # Waits for the job to complete

    table = client.get_table(table_ref)
    print('Loaded {} rows into {}:{}.'.format(table.num_rows, dataset_id, table_id))
```
```sh
CREATE TABLE your_dataset.your_table
(
    column1 STRING,
    column2 INTEGER,
    -- Add more columns as necessary
);

INSERT INTO your_dataset.your_table
SELECT *
FROM external_query(
    'your_project_id.your_dataset_id.your_table_id',
    'your_connection_name',
    'your_database_name',
    'your_username',
    'your_password'
);
```

#### Loading Data into BiqQuery using streaming 
- Details: Streaming data from Cloud Storage involves ingesting real-time data into BigQuery from files stored in Cloud Storage. It is suitable for scenarios where data is continuously updated or generated.
- Use Case: Analyzing user activity logs in real-time to identify patterns and take immediate actions.

            +-------------------+
            |    Cloud Storage  |
            +-------------------+
                      |
                      |
        +--------------+-------------+
        |                            |
        |     Cloud Pub/Sub          |
        |                            |
        +--------------+-------------+
                      |
                      |
          +-----------+-----------+
          |                       |
          |    BigQuery           |
          |                       |
          +-----------------------+
- Technique: Using Cloud Pub/Sub as an intermediary messaging service to receive streaming data from Cloud Storage and forwarding it to BigQuery.

```sh
from google.cloud import bigquery
from google.cloud import pubsub_v1

def stream_data_from_gcs_to_bigquery(project_id, dataset_id, table_id, topic_name):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    client = bigquery.Client()
    table_ref = client.dataset(dataset_id).table(table_id)

    def callback(message):
        data = message.data.decode('utf-8')
        print('Received message: {}'.format(data))

        # Transform data as needed
        transformed_data = transform_data(data)

        # Insert data into BigQuery
        errors = client.insert_rows_json(table_ref, [transformed_data])

        if errors:
            print('Encountered errors while inserting data: {}'.format(errors))
        else:
            print('Data inserted successfully into BigQuery.')

        message.ack()

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, topic_name)
    subscriber.subscribe(subscription_path, callback=callback)

    print('Streaming data from Cloud Storage to BigQuery...')

    while True:
        time.sleep(1)

def transform_data(data):
    # Perform necessary data transformation
    transformed_data = {
        'column1': data['field1'],
        'column2': data['field2'],
        # Add more transformed columns as necessary
    }

    return transformed_data
```

### Loading Data Streaming from Cloud SQL MySQL:
- Details: Streaming data from Cloud SQL MySQL involves capturing real-time changes from a MySQL database hosted on Cloud SQL and streaming them into BigQuery.
- Example Use Case: Capturing real-time customer activity data from an e-commerce website and visualizing it for monitoring and analysis.

        +-------------------+
        |    Cloud SQL      |
        |    (MySQL)        |
        +-------------------+
                  |
                  |
      +-----------+-----------+
      |                       |
      |    Cloud Pub/Sub      |
      |                       |
      +-----------+-----------+
                  |
                  |
        +---------+---------+
        |                   |
        |    BigQuery       |
        |                   |
        +-------------------+
- Technique: Using Cloud Pub/Sub to capture database change events from Cloud SQL and forwarding them to BigQuery.

```sh
import mysql.connector
from google.cloud import bigquery
from google.cloud import pubsub_v1

def stream_data_from_cloudsql_to_bigquery(project_id, dataset_id, table_id, topic_name):
    connection = mysql.connector.connect(
        host='your_cloudsql_host',
        user='your_username',
        password='your_password',
        database='your_database'
    )

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM your_table')

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    client = bigquery.Client()
    table_ref = client.dataset(dataset_id).table(table_id)

    for row in cursor.fetchall():
        data = transform_data(row)
        transformed_data = {
            'column1': data['field1'],
            'column2': data['field2'],
            # Add more transformed columns as necessary
        }

        publisher.publish(topic_path, transformed_data)

    print('Streaming data from Cloud SQL to BigQuery...')

def transform_data(data):
    # Perform necessary data transformation
    transformed_data = {
        'field1': data[0],
        'field2': data[1],
        # Add more transformed fields as necessary
    }

    return transformed_data
```

### Loading Data Streaming from External Data and APIs:
- Details: Streaming data from external sources and APIs involves capturing real-time events or data updates from external systems and streaming them into BigQuery.
- Use Case: Real-time sentiment analysis of social media data by capturing streaming tweets and analyzing them in BigQuery.

                   +-----------------+
                   |   External Data |
                   |   & APIs        |
                   +-----------------+
                             |
                             |
               +-------------+------------+
               |                          |
               |    Cloud Pub/Sub         |
               |                          |
               +-------------+------------+
                             |
                             |
                  +----------+----------+
                  |                     |
                  |    BigQuery         |
                  |                     |
                  +---------------------+
- Technique: Utilizing Cloud Pub/Sub to receive real-time events or data updates from external systems and streaming them into BigQuery.

```sh
from google.cloud import bigquery
from google.cloud import pubsub_v1
import json

def stream_data_from_external_sources_to_bigquery(project_id, dataset_id, table_id, topic_name):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    client = bigquery.Client()
    table_ref = client.dataset(dataset_id).table(table_id)

    def callback(message):
        data = json.loads(message.data.decode('utf-8'))
        print('Received message: {}'.format(data))

        # Transform data as needed
        transformed_data = transform_data(data)

        # Insert data into BigQuery
        errors = client.insert_rows_json(table_ref, [transformed_data])

        if errors:
            print('Encountered errors while inserting data: {}'.format(errors))
        else:
            print('Data inserted successfully into BigQuery.')

        message.ack()

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, topic_name)
    subscriber.subscribe(subscription_path, callback=callback)

    print('Streaming data from external sources to BigQuery...')

    while True:
        time.sleep(1)

def transform_data(data):
    # Perform necessary data transformation
    transformed_data = {
        'column1': data['field1'],
        'column2': data['field2'],
        # Add more transformed columns as necessary
    }

    return transformed_data
```