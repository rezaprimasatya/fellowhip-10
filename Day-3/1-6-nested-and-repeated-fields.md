# Nested Fields:

- Detail: Nested fields allow you to represent hierarchical and nested structures within a table. This is useful when dealing with complex data that contains nested objects or arrays.
- Technique: To create nested fields in BigQuery, you can define a STRUCT or RECORD data type to encapsulate nested fields within a table column.

```sh
CREATE TABLE example_table (
  id INT,
  name STRING,
  address STRUCT<
    street STRING,
    city STRING,
    country STRING
  >,
  orders ARRAY<STRUCT<
    order_id INT,
    product STRING,
    quantity INT
  >>
);
```
- Relation SQL: No specific relation SQL is required for nested fields.
```sh
SELECT
  id,
  name,
  address.street,
  address.city,
  address.country,
  order.order_id,
  order.product,
  order.quantity
FROM
  example_table,
  UNNEST(orders) AS order;
```
- Best Practice: Use nested fields when dealing with hierarchical or nested data structures. It improves data organization and reduces the need for complex joins.

# Repeated Fields:

- Detail: Repeated fields allow you to store multiple values within a single field. This is useful when dealing with scenarios where a column may contain multiple related values, such as tags or items in a list.
- Technique: To create repeated fields in BigQuery, you can define an ARRAY data type for a column that allows multiple values.

```sh
CREATE TABLE example_table (
  id INT,
  name STRING,
  tags ARRAY<STRING>
);
```
- Relation SQL: No specific relation SQL is required for repeated fields.

```sh
SELECT
  id,
  name,
  tag
FROM
  example_table,
  UNNEST(tags) AS tag;
```
- Best Practice: Use repeated fields when dealing with scenarios where a column may contain multiple related values. It simplifies data storage and querying for such cases.

# Advanced Table Definitions:
To define more advanced table structures with nested and repeated fields, you can utilize additional data types, such as STRUCT and ARRAY. This allows for nesting and repeating fields within fields, creating complex and flexible table structures.

# Advanced Query Logic:
With nested and repeated fields, you can leverage advanced query logic to perform more complex operations. This includes querying specific nested fields, performing aggregations on repeated fields, and using UNNEST to flatten repeated fields for further analysis.

For example, you can use the ARRAY_AGG function to aggregate repeated values into an array, or use subqueries to filter and aggregate data within nested fields.

```sh
-- Example: Aggregating repeated values into an array
SELECT
  id,
  name,
  ARRAY_AGG(tag) AS all_tags
FROM
  example_table,
  UNNEST(tags) AS tag
GROUP BY
  id,
  name;
```

By utilizing advanced table definitions and query logic, you can handle complex nested and repeated field structures efficiently and effectively in BigQuery.