# Partitioning:

### Step-by-Step:

- Determine the partitioning column: Identify the column that will be used for partitioning. It should be a column that is frequently used in filtering or joining operations.
- Choose the partitioning type: Decide on the partitioning type based on your data and query patterns. BigQuery supports partitioning by ingestion time or a specific column value.
- Create a partitioned table: Create a new table with partitioning enabled using the desired partitioning column and type.
- Load data into the partitioned table: Load or insert data into the partitioned table, ensuring that the data is properly partitioned based on the partitioning column value.

### Advanced Strategies:

- Date-based partitioning: Partition the table based on date values, such as by day, month, or year. This allows for efficient querying and data management for time-series data.
```sh
CREATE TABLE partitioned_table
PARTITION BY DATE(date_column)
OPTIONS(
  description = "Date-based partitioned table"
) AS
SELECT
  *
FROM
  source_table;

```

```sh
SELECT
  *
FROM
  partitioned_table
WHERE
  DATE(date_column) = '2023-01-01';
```

- Range-based partitioning: Partition the table based on specific ranges or intervals of a numeric or date column. This strategy is useful for optimizing queries that involve range-based filtering.
```sh
CREATE TABLE partitioned_table
PARTITION BY RANGE(age)
(
  PARTITION p0 VALUES LESS THAN (18),
  PARTITION p1 VALUES LESS THAN (25),
  PARTITION p2 VALUES LESS THAN (40),
  PARTITION p3 VALUES LESS THAN (MAXVALUE)
)
OPTIONS(
  description = "Range-based partitioned table"
) AS
SELECT
  *
FROM
  source_table;

```
```sh
SELECT
  *
FROM
  partitioned_table
WHERE
  age < 25;

```
- Composite partitioning: Combine multiple partitioning columns to create a composite partition key. 
```sh
CREATE TABLE partitioned_table
PARTITION BY (date_column, country)
OPTIONS(
  description = "Composite partitioned table"
) AS
SELECT
  *
FROM
  source_table;

```
```sh
SELECT
  *
FROM
  partitioned_table
WHERE
  date_column = '2023-01-01'
  AND country = 'USA';

```

This strategy provides more granular control over data segmentation.
```sh
+----------------------+
|    Partitioned Table  |
+-----------+----------+
            |
            |
+-----------+-----------+
|                       |
|   Partition Columns   |
|                       |
+-----------------------+
```
### Technique:
```sh
CREATE TABLE partitioned_table
PARTITION BY DATE(timestamp_column)
OPTIONS(
  description = "Partitioned table"
) AS
SELECT
  *
FROM
  source_table;
```sh

### Query SQL: Querying a partitioned table in BigQuery:

```sh
SELECT
  *
FROM
  partitioned_table
WHERE
  DATE(timestamp_column) = '2023-01-01';
```
- Best Practice: Partition tables based on frequently used filtering or joining columns to optimize query performance and reduce costs. Use the PARTITION BY clause to define the partitioning column and type during table creation.

# Clustering:

### Step-by-Step:

- Determine the clustering columns: Identify the columns that will be used for clustering. These should be columns commonly used in filtering, grouping, or joining operations.
- Create a clustered table: Create a new table with clustering enabled, specifying the clustering columns.
- Load data into the clustered table: Load or insert data into the clustered table. BigQuery will automatically cluster the data based on the specified columns.

### Advanced Strategies:

- Multi-level clustering: Use multiple columns for clustering to further optimize query performance by creating hierarchical clusters.
```sh
CREATE TABLE clustered_table
CLUSTER BY column1, column2
OPTIONS(
  description = "Multi-level clustered table"
) AS
SELECT
  *
FROM
  source_table;

```
```sh
SELECT
  *
FROM
  clustered_table
WHERE
  column1 = 'value1'
ORDER BY
  column2;

```

- Clustered materialized views: Create materialized views on top of clustered tables to further enhance query performance and speed up query execution.
```sh
CREATE MATERIALIZED VIEW mv_table
CLUSTER BY column1, column2
OPTIONS(
  description = "Clustered materialized view"
) AS
SELECT
  column1,
  column2,
  COUNT(*) AS count
FROM
  source_table
GROUP BY
  column1,
  column2;

```

```sh
SELECT
  *
FROM
  mv_table
WHERE
  column1 = 'value1';

```


```sh
+----------------------+
|    Clustered Table    |
+-----------+----------+
            |
            |
+-----------+-----------+
|                       |
|  Clustering Columns   |
|                       |
+-----------------------+
```
```sh
CREATE TABLE clustered_table
CLUSTER BY column1, column2
OPTIONS(
  description = "Clustered table"
) AS
SELECT
  *
FROM
  source_table;
```
Query SQL: Querying a clustered table in BigQuery:
```sh
SELECT
  *
FROM
  clustered_table
WHERE
  column1 = 'value1'
ORDER BY
  column2;
```

- Best Practice: Cluster tables based on frequently used filtering, grouping, or joining columns to optimize query performance. Use the CLUSTER BY clause to define the clustering columns during table creation.

- Creating or Altering Partitions and Clusters on New Table:
To create a new table with partitions or clusters, you can use the respective clauses (PARTITION BY and CLUSTER BY) during the table creation statement.

- Creating or Altering Partitions on Existing Table:
To add partitions to an existing table, you can use the ALTER TABLE statement with the ADD PARTITION clause. This allows you to define additional partitions based on specific criteria.

- Creating or Altering Clusters on Existing Table:
Currently, BigQuery does not support altering the clustering of an existing table. To apply clustering to an existing table, you would need to create a new clustered table and load the data from the existing table into the new table.

- Note: Creating or altering partitions and clusters on large-scale tables can have cost and performance implications. Carefully consider your data size, query patterns, and specific use cases before applying these techniques.