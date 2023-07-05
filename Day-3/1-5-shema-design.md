# Star Schema:
- Advanced Details: Star schema is a simple and widely used dimensional modeling technique in data warehousing. It consists of a central fact table connected to multiple dimension tables. The fact table contains measures or metrics, while dimension tables provide descriptive attributes for analysis.


          +------------------+
          |    Fact Table    |
          +-------+----------+
                  |
                  |
      +-----------+-----------+
      |                       |
      |    Dimension Tables   |
      |                       |
      +-----------------------+
```sh
-- Fact Table
CREATE TABLE fact_table (
  fact_id INT,
  dimension_id INT,
  measure_1 INT,
  measure_2 FLOAT,
  -- Add more measures as necessary
  PRIMARY KEY (fact_id),
  FOREIGN KEY (dimension_id) REFERENCES dimension_table(dimension_id)
);

-- Dimension Tables
CREATE TABLE dimension_table (
  dimension_id INT,
  attribute_1 STRING,
  attribute_2 STRING,
  -- Add more attributes as necessary
  PRIMARY KEY (dimension_id)
);
```
Relation SQL: Establishing the relationship between the fact table and dimension table:
```sh
ALTER TABLE fact_table
ADD FOREIGN KEY (dimension_id) REFERENCES dimension_table(dimension_id);
```
Query SQL: Querying a star schema in BigQuery:
```sh
SELECT
  dimension_table.attribute_1,
  SUM(fact_table.measure_1) AS total_measure
FROM
  fact_table
JOIN
  dimension_table ON fact_table.dimension_id = dimension_table.dimension_id
GROUP BY
  dimension_table.attribute_1;
```

- Best Practice: Denormalize dimension tables to avoid complex joins and improve query performance. Use surrogate keys for dimension tables to ensure stability even when attributes change.

# Snowflake Schema:
- Advanced Details: Snowflake schema is an extension of the star schema, where dimension tables are further normalized into sub-dimension tables. This enables more granular data modeling at the expense of increased complexity.

          +------------------+
          |    Fact Table    |
          +-------+----------+
                  |
                  |
      +-----------+-----------+
      |                       |
      |    Dimension Tables   |
      |       (Normalized)    |
      +-----------+-----------+
                  |
                  |
      +-----------+-----------+
      |                       |
      |   Sub-Dimension Tables |
      |       (Normalized)    |
      +-----------------------+
```sh
-- Fact Table
CREATE TABLE fact_table (
  fact_id INT,
  dimension_id INT,
  measure_1 INT,
  measure_2 FLOAT,
  -- Add more measures as necessary
  PRIMARY KEY (fact_id),
  FOREIGN KEY (dimension_id) REFERENCES dimension_table(dimension_id)
);

-- Dimension Tables (Normalized)
CREATE TABLE dimension_table (
  dimension_id INT,
  attribute_1 STRING,
  attribute_2 STRING,
  -- Add more attributes as necessary
  PRIMARY KEY (dimension_id)
);

-- Sub-Dimension Tables (Normalized)
CREATE TABLE sub_dimension_table (
  sub_dimension_id INT,
  dimension_id INT,
  attribute_1 STRING,
  -- Add more attributes as necessary
  PRIMARY KEY (sub_dimension_id),
  FOREIGN KEY (dimension_id) REFERENCES dimension_table(dimension_id)
);
```
Relation SQL: Establishing relationships between tables in a snowflake schema:
```sh
ALTER TABLE fact_table
ADD FOREIGN KEY (dimension_id) REFERENCES dimension_table(dimension_id);

ALTER TABLE sub_dimension_table
ADD FOREIGN KEY (dimension_id) REFERENCES dimension_table(dimension_id);
```

Query SQL: Querying a snowflake schema in BigQuery:
```sh
SELECT
  dimension_table.attribute_1,
  SUM(fact_table.measure_1) AS total_measure
FROM
  fact_table
JOIN
  dimension_table ON fact_table.dimension_id = dimension_table.dimension_id
JOIN
  sub_dimension_table ON dimension_table.dimension_id = sub_dimension_table.dimension_id
GROUP BY
  dimension_table.attribute_1;
```
- Best Practice: Balance between normalization and denormalization based on the complexity of data relationships and query patterns. Normalize dimension tables for shared attributes and create separate sub-dimension tables for specific attributes.

# Galaxy Schema:
- Advanced Details: Galaxy schema is an extension of the star schema, where multiple fact tables share dimension tables. It is suitable for scenarios where there are multiple related fact tables that need to share common dimensions.

          +------------------+
          |   Fact Table 1   |
          +-------+----------+
                  |
                  |
      +-----------+-----------+
      |                       |
      |    Dimension Tables   |
      |                       |
      +-----------+-----------+
                  |
                  |
      +-----------+-----------+
      |                       |
      |    Dimension Tables   |
      |                       |
      +-----------+-----------+
                  |
                  |
          +------------------+
          |   Fact Table 2   |
          +------------------+
```sh
-- Fact Table 1
CREATE TABLE fact_table_1 (
  fact_id INT,
  dimension_id INT,
  measure_1 INT,
  measure_2 FLOAT,
  -- Add more measures as necessary
  PRIMARY KEY (fact_id),
  FOREIGN KEY (dimension_id) REFERENCES dimension_table(dimension_id)
);

-- Fact Table 2
CREATE TABLE fact_table_2 (
  fact_id INT,
  dimension_id INT,
  measure_3 INT,
  measure_4 FLOAT,
  -- Add more measures as necessary
  PRIMARY KEY (fact_id),
  FOREIGN KEY (dimension_id) REFERENCES dimension_table(dimension_id)
);

-- Dimension Tables
CREATE TABLE dimension_table (
  dimension_id INT,
  attribute_1 STRING,
  attribute_2 STRING,
  -- Add more attributes as necessary
  PRIMARY KEY (dimension_id)
);
```

Relation SQL: Establishing relationships between fact tables and dimension table in a galaxy schema:
```sh
ALTER TABLE fact_table_1
ADD FOREIGN KEY (dimension_id) REFERENCES dimension_table(dimension_id);

ALTER TABLE fact_table_2
ADD FOREIGN KEY (dimension_id) REFERENCES dimension_table(dimension_id);
```
Query SQL: Querying a galaxy schema in BigQuery:
```sh
SELECT
  dimension_table.attribute_1,
  SUM(fact_table_1.measure_1) AS total_measure_1,
  SUM(fact_table_2.measure_3) AS total_measure_2
FROM
  fact_table_1
JOIN
  dimension_table ON fact_table_1.dimension_id = dimension_table.dimension_id
JOIN
  fact_table_2 ON fact_table_1.dimension_id = fact_table_2.dimension_id
GROUP BY
  dimension_table.attribute_1;
```
- Best Practice: Ensure dimension tables are shared accurately between fact tables. Consider the balance between reusability and specific dimension requirements for each fact table.

# Fact Constellation Schema:
- Advanced Details: Fact constellation schema is an extension of the star schema, where multiple fact tables share dimension tables, and additional dimension tables are connected to each fact table individually.

           +------------------+
           |   Fact Table 1   |
           +-------+----------+
                   |
                   |
       +-----------+-----------+
       |                       |
       |    Dimension Tables   |
       |                       |
       +-----------------------+
                   |
                   |
       +-----------+-----------+
       |                       |
       |    Dimension Tables   |
       |                       |
       +-----------+-----------+
                   |
                   |
           +-------+----------+
           |   Fact Table 2   |
           +------------------+
```sh
-- Fact Table 1
CREATE TABLE fact_table_1 (
  fact_id INT,
  dimension_id_1 INT,
  dimension_id_2 INT,
  measure_1 INT,
  measure_2 FLOAT,
  -- Add more measures as necessary
  PRIMARY KEY (fact_id),
  FOREIGN KEY (dimension_id_1) REFERENCES dimension_table_1(dimension_id),
  FOREIGN KEY (dimension_id_2) REFERENCES dimension_table_2(dimension_id)
);

-- Fact Table 2
CREATE TABLE fact_table_2 (
  fact_id INT,
  dimension_id_3 INT,
  measure_3 INT,
  measure_4 FLOAT,
  -- Add more measures as necessary
  PRIMARY KEY (fact_id),
  FOREIGN KEY (dimension_id_3) REFERENCES dimension_table_3(dimension_id)
);

-- Dimension Tables 1
CREATE TABLE dimension_table_1 (
  dimension_id INT,
  attribute_1 STRING,
  attribute_2 STRING,
  -- Add more attributes as necessary
  PRIMARY KEY (dimension_id)
);

-- Dimension Tables 2
CREATE TABLE dimension_table_2 (
  dimension_id INT,
  attribute_3 STRING,
  attribute_4 STRING,
  -- Add more attributes as necessary
  PRIMARY KEY (dimension_id)
);

-- Dimension Tables 3
CREATE TABLE dimension_table_3 (
  dimension_id INT,
  attribute_5 STRING,
  attribute_6 STRING,
  -- Add more attributes as necessary
  PRIMARY KEY (dimension_id)
);
```
- Relation SQL: Establishing relationships between fact tables and dimension tables in a fact constellation schema:
```sh
ALTER TABLE fact_table_1
ADD FOREIGN KEY (dimension_id_1) REFERENCES dimension_table_1(dimension_id),
ADD FOREIGN KEY (dimension_id_2) REFERENCES dimension_table_2(dimension_id);

ALTER TABLE fact_table_2
ADD FOREIGN KEY (dimension_id_3) REFERENCES dimension_table_3(dimension_id);
```
- Query SQL: Querying a fact constellation schema in BigQuery:
```sh
SELECT
  dimension_table_1.attribute_1,
  dimension_table_2.attribute_3,
  SUM(fact_table_1.measure_1) AS total_measure_1,
  SUM(fact_table_2.measure_3) AS total_measure_2
FROM
  fact_table_1
JOIN
  dimension_table_1 ON fact_table_1.dimension_id_1 = dimension_table_1.dimension_id
JOIN
  dimension_table_2 ON fact_table_1.dimension_id_2 = dimension_table_2.dimension_id
JOIN
  fact_table_2 ON fact_table_1.dimension_id_1 = fact_table_2.dimension_id_3
GROUP BY
  dimension_table_1.attribute_1,
  dimension_table_2.attribute_3;
```
- Best Practice: Carefully define relationships between fact tables and dimension tables. Consider the specific dimension requirements for each fact table and ensure proper joins for accurate analysis.

# Star Cluster Schema:
- Advanced Details: Star cluster schema is an extension of the star schema, where multiple fact tables share dimension tables, and each fact table has its set of dimension tables.

          +------------------+
          |   Fact Table 1   |
          +-------+----------+
                  |
                  |
      +-----------+-----------+
      |                       |
      |    Dimension Tables   |
      |       (Shared)        |
      +-----------+-----------+
                  |
                  |
          +------------------+
          |   Fact Table 2   |
          +------------------+
                  |
                  |
      +-----------+-----------+
      |                       |
      |   Sub-Dimension Tables |
      |       (Specific)      |
      +-----------------------+

```sh
-- Fact Table 1
CREATE TABLE fact_table_1 (
  fact_id INT,
  dimension_id_1 INT,
  measure_1 INT,
  measure_2 FLOAT,
  -- Add more measures as necessary
  PRIMARY KEY (fact_id),
  FOREIGN KEY (dimension_id_1) REFERENCES dimension_table(dimension_id)
);

-- Fact Table 2
CREATE TABLE fact_table_2 (
  fact_id INT,
  dimension_id_2 INT,
  measure_3 INT,
  measure_4 FLOAT,
  -- Add more measures as necessary
  PRIMARY KEY (fact_id),
  FOREIGN KEY (dimension_id_2) REFERENCES sub_dimension_table(dimension_id)
);

-- Dimension Tables (Shared)
CREATE TABLE dimension_table (
  dimension_id INT,
  attribute_1 STRING,
  attribute_2 STRING,
  -- Add more attributes as necessary
  PRIMARY KEY (dimension_id)
);

-- Sub-Dimension Tables (Specific)
CREATE TABLE sub_dimension_table (
  dimension_id INT,
  attribute_3 STRING,
  -- Add more attributes as necessary
  PRIMARY KEY (dimension_id)
);
```
- Relation SQL: Establishing relationships between fact tables and dimension tables in a star cluster 
```sh
ALTER TABLE fact_table_1
ADD FOREIGN KEY (dimension_id_1) REFERENCES dimension_table(dimension_id);

ALTER TABLE fact_table_2
ADD FOREIGN KEY (dimension_id_2) REFERENCES sub_dimension_table(dimension_id);
```
- Query SQL: Querying a star cluster schema in BigQuery:
```sh
SELECT
  dimension_table.attribute_1,
  SUM(fact_table_1.measure_1) AS total_measure_1,
  SUM(fact_table_2.measure_3) AS total_measure_2
FROM
  fact_table_1
JOIN
  dimension_table ON fact_table_1.dimension_id_1 = dimension_table.dimension_id
JOIN
  fact_table_2 ON fact_table_2.dimension_id_2 = sub_dimension_table.dimension_id
GROUP BY
  dimension_table.attribute_1;
```
- Best Practice: Share common dimensions among fact tables in the shared dimension tables, and use sub-dimension tables for specific attributes of each fact table. Consider the balance between reusability and specific dimension requirements.