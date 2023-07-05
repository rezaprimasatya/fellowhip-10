A data warehouse is a centralized and integrated repository of structured, historical, and potentially large volumes of data that is used for reporting, analytics, and decision-making purposes. It serves as a single source of truth for an organization's data, providing a consistent and reliable foundation for data analysis and business intelligence.

# Concepts:
- Extract, Transform, Load (ETL): 
    - Data from various sources is extracted, transformed into a suitable format, and loaded into the data warehouse.

    ```sh
    +-------------+          +-------------+         +----------------+
    |  Extraction   | -------->|  Transformation        |-------->|     Loading         |
    |    (Source)   |          |       (ETL)            |          (Data Warehouse)     |
    +-------------+          +-------------+         +----------------+

    ```

    ```sh
    # Extract data from a CSV file
    def extract_data(file_path):
        data = []
        with open(file_path, 'r') as file:
            for line in file:
                data.append(line.strip())
        return data

    # Transform data by converting it to uppercase
    def transform_data(data):
        transformed_data = [item.upper() for item in data]
        return transformed_data

    # Load data into the data warehouse
    def load_data(warehouse_conn, transformed_data):
        for item in transformed_data:
            warehouse_conn.execute(f"INSERT INTO table_name VALUES ('{item}')")

    ```
- Dimensional Modeling: 
    - A data modeling technique that organizes data into dimensions and facts, enabling efficient querying and analysis.

    ```sh
              +---------------+
          |   Dimension   |
          |    Table 1    |
          +---------------+
            |
            |
            |    +-------+
            +--->|  Fact  |
                 |  Table  |
                 +-------+

    ```

    ```sh
    - SQL Script Example:
        ```sql
        -- Dimension Table
        CREATE TABLE dimension_table1 (
            dimension_id INT PRIMARY KEY,
            dimension_attribute1 VARCHAR(50),
            dimension_attribute2 VARCHAR(50),
            ...
        );
        
        -- Fact Table
        CREATE TABLE fact_table (
            fact_id INT PRIMARY KEY,
            dimension_id INT,
            measure1 INT,
            measure2 FLOAT,
            ...
            FOREIGN KEY (dimension_id) REFERENCES dimension_table1(dimension_id)
        );

    ```

- Star Schema: 
    - A common dimensional modeling schema where a central fact table is surrounded by dimension tables.

    ```sh
              +-----------------+
          |   Dimension 1  |
          +-----------------+
            |
            |
            |      +-------+
            +----->|  Fact  |
            |     |  Table  |
            |     +-------+
            |
            |
          +-----------------+
          |   Dimension 2  |
          +-----------------+

    ```

    ```sh
    - SQL Script Example:
    ```sql
    -- Dimension Table 1
    CREATE TABLE dimension_table1 (
        dimension1_id INT PRIMARY KEY,
        dimension1_attribute1 VARCHAR(50),
        dimension1_attribute2 VARCHAR(50),
        ...
    );
    
    -- Fact Table
    CREATE TABLE fact_table (
        fact_id INT PRIMARY KEY,
        dimension1_id INT,
        dimension2_id INT,
        measure1 INT,
        measure2 FLOAT,
        ...
        FOREIGN KEY (dimension1_id) REFERENCES dimension_table1(dimension1_id),
        FOREIGN KEY (dimension2_id) REFERENCES dimension_table2(dimension2_id)
    );

    ```

- Snowflake Schema: 
    - A dimensional modeling schema where dimension tables are normalized into multiple related tables.
    ```sh
              +-------------------+
          |   Dimension 1    |
          +-------------------+
            |
            |
            |        +-----------+
            +------->| Dimension |
            |       |   Table 2  |
            |       +-----------+
            |
            |
          +-------------------+
          |   Dimension 3    |
          +-------------------+

    ```

    ```sh
    - SQL Script Example:
    ```sql
    -- Dimension Table 1
    CREATE TABLE dimension_table1 (
        dimension1_id INT PRIMARY KEY,
        dimension1_attribute1 VARCHAR(50),
        dimension1_attribute2 VARCHAR(50),
        ...
    );
    
    -- Dimension Table 2
    CREATE TABLE dimension_table2 (
        dimension2_id INT PRIMARY KEY,
        dimension2_attribute1 VARCHAR(50),
        dimension2_attribute2 VARCHAR(50),
        ...
    );
    
    -- Fact Table
    CREATE TABLE fact_table (
        fact_id INT PRIMARY KEY,
        dimension1_id INT,
        dimension2_id INT,
        dimension3_id INT,
        measure1 INT,
        measure2 FLOAT,
        ...
        FOREIGN KEY (dimension1_id) REFERENCES dimension_table1(dimension1_id),
        FOREIGN KEY (dimension2_id) REFERENCES dimension_table2(dimension2_id),
        FOREIGN KEY (dimension3_id) REFERENCES dimension_table3(dimension3_id)
    );

    ```
- Aggregates: 
    - Pre-calculated summaries of data that improve query performance for common analytical queries.
    ```sh
    -- Create Aggregate Table
    CREATE TABLE aggregate_table (
        dimension_id INT PRIMARY KEY,
        aggregate_measure1 INT,
        aggregate_measure2 FLOAT,
        ...
    );

    -- Refresh Aggregate Data
    INSERT INTO aggregate_table (dimension_id, aggregate_measure1, aggregate_measure2, ...)
    SELECT dimension_id, SUM(measure1), AVG(measure2), ...
    FROM fact_table
    GROUP BY dimension_id;

    ```


### How does it work?

Data warehouses work by consolidating and transforming data from various sources into a unified and structured format for analysis.
The ETL processes extract data from the sources, apply transformations to clean, integrate, and standardize the data, and then load it into the data warehouse.
Once the data is loaded, it is organized in a way that supports efficient querying and analysis.
Users can then use reporting and analysis tools to query the data warehouse and derive insights from the consolidated data.

- Data Extraction:
    - Data extraction involves retrieving data from various sources, such as transactional databases, external systems, or data lakes.

    ```sh
       +----------------------+
   | Transactional        |
   | Databases            |
   +----------+-----------+
              |
              |
   +----------+-----------+
   | Data Lakes            |
   +----------------------+

    ```

    ```sh
    import psycopg2
    import pandas as pd

    def extract_data_from_transactional_db():
        connection = psycopg2.connect(
            host="database_host",
            database="database_name",
            user="username",
            password="password"
        )
        cursor = connection.cursor()
        
        # Execute SQL queries to extract data from the transactional databases
        cursor.execute("SELECT * FROM table1")
        data = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return data

    def extract_data_from_data_lake():
        # Code for extracting data from the data lake
        data = pd.read_csv("data_lake.csv")
        
        return data

    # Extract data from the transactional databases
    data_from_db = extract_data_from_transactional_db()

    # Extract data from the data lake
    data_from_lake = extract_data_from_data_lake()

    ```

- Data Transformation:
    - Data transformation involves cleaning, integrating, and standardizing the extracted data to ensure consistency and usability for analysis.

    ```sh
    def clean_data(data):
    # Code for cleaning and standardizing data
    cleaned_data = perform_data_cleaning(data)
    
    return cleaned_data

    def integrate_data(data_from_db, data_from_lake):
        # Code for integrating and merging data from multiple sources
        integrated_data = merge_data(data_from_db, data_from_lake)
        
        return integrated_data

    # Clean the extracted data
    cleaned_data = clean_data(data_from_db)

    # Integrate the cleaned data from multiple sources
    integrated_data = integrate_data(cleaned_data, data_from_lake)

    ```

- Data Loading:
    - Data loading involves loading the transformed and integrated data into the data warehouse for storage and analysis.

    ```sh
       +--------------------+
   | Data Warehouse     |
   | (RDBMS - PostgreSQL)|
   +--------------------+

    ```

    ```sh
    import psycopg2

    def load_data_into_data_warehouse(data):
        connection = psycopg2.connect(
            host="data_warehouse_host",
            database="data_warehouse_name",
            user="username",
            password="password"
        )
        cursor = connection.cursor()
        
        # Load the transformed and integrated data into the data warehouse
        for row in data:
            cursor.execute("INSERT INTO data_warehouse_table VALUES (%s, %s, %s)", row)
        
        connection.commit()
        cursor.close()
        connection.close()

    # Load the integrated data into the data warehouse
    load_data_into_data_warehouse(integrated_data)

    ```

- Data Querying and Analysis:
    - Once the data is loaded into the data warehouse, users can query and analyze it using SQL or other analysis tools.

    ```sh
    -- Query to calculate total sales by product category
    SELECT
        category,
        SUM(sales) AS total_sales
    FROM
        data_warehouse_table
    GROUP BY
        category
    ORDER BY
        total_sales DESC;

    ```

### Type of Keys

- Primary Key:
    - Details: A primary key is a unique identifier for each record in a table. It ensures data integrity by enforcing uniqueness and providing a means to identify individual records.
    - Use Case: Primary keys are commonly used to establish relationships between tables and enable efficient data retrieval.
```sh
CREATE TABLE Customers (
  CustomerID INT PRIMARY KEY,
  CustomerName VARCHAR(50),
  Email VARCHAR(50)
);
```
```sh
CREATE TABLE Orders (
  OrderID INT PRIMARY KEY,
  CustomerID INT,
  OrderDate DATE,
  FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);
```
```sh
SELECT o.OrderID, o.OrderDate, c.CustomerName, c.Email
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
WHERE o.OrderID = 12345;
```

- Foreign Key:
    - Details: A foreign key is a field in a table that refers to the primary key of another table, establishing a relationship between the two tables.
    - Use Case: Foreign keys are used to enforce referential integrity and maintain data consistency across related tables.
```sh
CREATE TABLE Customers (
  CustomerID INT PRIMARY KEY,
  CustomerName VARCHAR(50),
  Email VARCHAR(50)
);
```
```sh
CREATE TABLE Orders (
  OrderID INT PRIMARY KEY,
  CustomerID INT,
  OrderDate DATE,
  FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);
```
```sh
SELECT o.OrderID, o.OrderDate
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
WHERE c.CustomerName = 'John Doe';
```
- Surrogate Key:
- Details: A surrogate key is a system-generated key used as a substitute for a natural key to uniquely identify records in a table.
- Use Case: Surrogate keys are beneficial when there is no suitable natural key available or when the natural key is complex or subject to change.

```sh
CREATE TABLE Employees (
  EmployeeID INT PRIMARY KEY,
  EmployeeName VARCHAR(50),
  Email VARCHAR(50)
);
```
```sh
INSERT INTO Employees (EmployeeName, Email)
VALUES ('John Doe', 'johndoe@example.com');
```
- Composite Key:
- Details: A composite key is a key that consists of two or more columns in a table to uniquely identify records.
- Use Case: Composite keys are useful when a single column does not provide enough uniqueness, and a combination of columns is required for record identification.

```sh
CREATE TABLE Orders (
  OrderID INT,
  ProductID INT,
  OrderDate DATE,
  PRIMARY KEY (OrderID, ProductID)
);
```
```sh
SELECT *
FROM Orders
WHERE OrderID = 12345 AND ProductID = 6789;
```
- Candidate Key:
- Details: A candidate key is a unique key that can uniquely identify each record in a table but is not chosen as the primary key.
- Use Case: Candidate keys are alternative keys that could be chosen as the primary key but are not selected for various reasons, such as simplicity or business rules.

```sh
CREATE TABLE Students (
  StudentID INT PRIMARY KEY,
  StudentName VARCHAR(50),
  SSN VARCHAR(9) UNIQUE,
  Email VARCHAR(50) UNIQUE
);
```
```sh
SELECT *
FROM Students
WHERE SSN = '123456789';
```

- Super Key:
- Details: A super key is a set of one or more columns that can uniquely identify a record in a table.
- Use Case: Super keys provide a broader concept of uniqueness but may contain redundant attributes that are not necessary for unique identification.


```sh
CREATE TABLE Employees (
  EmployeeID INT,
  EmployeeName VARCHAR(50),
  Email VARCHAR(50),
  SSN VARCHAR(9),
  PRIMARY KEY (EmployeeID),
  UNIQUE (Email, SSN)
);
```

```sh
SELECT *
FROM Employees
WHERE Email = 'johndoe@example.com' AND SSN = '123456789';
```

- Alternate Key:
- Details: An alternate key is a candidate key that is not chosen as the primary key but can be used as an alternative unique identifier.
- Use Case: Alternate keys provide additional options for record identification and can be useful in certain data retrieval scenarios.

```sh
CREATE TABLE Products (
  ProductID INT PRIMARY KEY,
  ProductCode VARCHAR(10) UNIQUE,
  ProductName VARCHAR(50),
  UPC VARCHAR(12) UNIQUE
);
```

```sh
SELECT *
FROM Products
WHERE ProductCode = 'ABC123';
```

- Artificial Key:
    - Details: An artificial key is a key that is created solely for identification purposes and does not have any inherent meaning.
    - Use Case: Artificial keys are typically used when there is no natural or meaningful attribute available to serve as a key.

```sh
CREATE TABLE Customers (
  CustomerID INT PRIMARY KEY,
  CustomerCode VARCHAR(10),
  CustomerName VARCHAR(50)
);
```
```sh
SELECT *
FROM Customers
WHERE CustomerCode = 'CUST001';
```