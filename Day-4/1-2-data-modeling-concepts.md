# Datawarehouse schemas:
- Star Schema
- Snowflake Schema
- Galaxy Schema
- Fact Constellation Schema
- Star Cluster Schema

Types of Dimensions in Data Warehouse Model
- Conformed Dimension
- Outrigger Dimension
- Shrunken Dimension
- Role-Playing Dimension
- Dimension to Dimension Table
- Junk Dimension
- Degenerate Dimension
- Swappable Dimension
- Step Dimension


# Start Schema

### Conformed Dimension:
A conformed dimension is a dimension that is shared and consistent across multiple fact tables.
```sh
-- Create Conformed Dimension table
CREATE TABLE dim_customer (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(100),
  customer_address VARCHAR(200),
  -- Other dimension attributes
);

-- Insert data into Conformed Dimension table
INSERT INTO dim_customer (customer_id, customer_name, customer_address)
VALUES
  (1, 'John Doe', '123 Main St'),
  (2, 'Jane Smith', '456 Elm St');
  
-- Create relation between Conformed Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_customer
FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id);

-- Manipulate data in Conformed Dimension table
UPDATE dim_customer
SET customer_address = '789 Oak Ave'
WHERE customer_id = 2;
```

### Outrigger Dimension:
An outrigger dimension is a dimension that is related to another dimension and provides additional attributes.
```sh
-- Create Outrigger Dimension table
CREATE TABLE dim_product_category (
  product_id INT PRIMARY KEY,
  category_id INT,
  category_name VARCHAR(50),
  -- Other dimension attributes
);

-- Insert data into Outrigger Dimension table
INSERT INTO dim_product_category (product_id, category_id, category_name)
VALUES
  (1, 101, 'Electronics'),
  (2, 102, 'Clothing');
  
-- Create relation between Outrigger Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_product_category
FOREIGN KEY (product_id) REFERENCES dim_product_category(product_id);

-- Manipulate data in Outrigger Dimension table
UPDATE dim_product_category
SET category_name = 'Accessories'
WHERE product_id = 2;
```

### Shrunken Dimension:
A shrunken dimension combines multiple low-cardinality dimensions into a single dimension table.
```sh
-- Create Shrunken Dimension table
CREATE TABLE dim_date (
  date_id INT PRIMARY KEY,
  day INT,
  month INT,
  year INT,
  -- Other dimension attributes
);

-- Insert data into Shrunken Dimension table
INSERT INTO dim_date (date_id, day, month, year)
VALUES
  (1, 1, 1, 2023),
  (2, 2, 1, 2023);
  
-- Create relation between Shrunken Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_date
FOREIGN KEY (date_id) REFERENCES dim_date(date_id);

-- Manipulate data in Shrunken Dimension table
UPDATE dim_date
SET year = 2022
WHERE date_id = 2;
```

### Role-Playing Dimension:
A role-playing dimension represents the same dimension table but with different roles or perspectives.

```sh
-- Create Role-Playing Dimension table
CREATE TABLE dim_date (
  date_id INT PRIMARY KEY,
  day INT,
  month INT,
  year INT,
  -- Other dimension attributes
);

-- Insert data into Role-Playing Dimension table
INSERT INTO dim_date (date_id, day, month, year)
VALUES
  (1, 1, 1, 2023),
  (2, 2, 1, 2023);
  
-- Create relation between Role-Playing Dimension and Fact table (e.g., Order Date)
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_order_date
FOREIGN KEY (order_date_id) REFERENCES dim_date(date_id);

-- Create relation between Role-Playing Dimension and Fact table (e.g., Ship Date)
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_ship_date
FOREIGN KEY (ship_date_id) REFERENCES dim_date(date_id);

-- Manipulate data in Role-Playing Dimension table
UPDATE dim_date
SET year = 2022
WHERE date_id = 2;
```

### Dimension to Dimension Table:
A dimension to dimension table represents a hierarchical relationship between dimensions.
```sh
-- Create Dimension to Dimension Table
CREATE TABLE dim_product_hierarchy (
  product_id INT PRIMARY KEY,
  parent_product_id INT,
  product_name VARCHAR(100),
  -- Other dimension attributes
);

-- Insert data into Dimension to Dimension Table
INSERT INTO dim_product_hierarchy (product_id, parent_product_id, product_name)
VALUES
  (1, NULL, 'Electronics'),
  (2, 1, 'Smartphones'),
  (3, 1, 'Laptops');
  
-- Create relation between Dimension to Dimension Table and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_product_hierarchy
FOREIGN KEY (product_id) REFERENCES dim_product_hierarchy(product_id);

-- Manipulate data in Dimension to Dimension Table
UPDATE dim_product_hierarchy
SET product_name = 'Mobile Phones'
WHERE product_id = 2;
```

### Junk Dimension:
A junk dimension combines multiple low-cardinality flags or indicators into a single dimension table.
```sh
-- Create Junk Dimension table
CREATE TABLE dim_flags (
  flag_id INT PRIMARY KEY,
  is_active BOOLEAN,
  is_promotion BOOLEAN,
  -- Other flag attributes
);

-- Insert data into Junk Dimension table
INSERT INTO dim_flags (flag_id, is_active, is_promotion)
VALUES
  (1, TRUE, FALSE),
  (2, TRUE, TRUE);
  
-- Create relation between Junk Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_flags
FOREIGN KEY (flag_id) REFERENCES dim_flags(flag_id);

-- Manipulate data in Junk Dimension table
UPDATE dim_flags
SET is_promotion = TRUE
WHERE flag_id = 2;
```

### Degenerate Dimension:
A degenerate dimension represents a dimension attribute that exists only in the fact table.
```sh
-- Create Fact table with Degenerate Dimension
CREATE TABLE fact_sales (
  sale_id INT PRIMARY KEY,
  product_id INT,
  quantity INT,
  -- Other fact attributes
  order_number VARCHAR(20) -- Degenerate dimension
);

-- Insert data into Fact table
INSERT INTO fact_sales (sale_id, product_id, quantity, order_number)
VALUES
  (1, 101, 5, 'ORD001'),
  (2, 102, 3, 'ORD002');
  
-- Manipulate data in Fact table with Degenerate Dimension
UPDATE fact_sales
SET order_number = 'ORD003'
WHERE sale_id = 2;
```

### Swappable Dimension:
A swappable dimension allows for multiple dimension tables to be used interchangeably.
```sh
-- Create Swappable Dimension table (e.g., Customer)
CREATE TABLE dim_customer (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(100),
  customer_address VARCHAR(200),
  -- Other dimension attributes
);

-- Create Swappable Dimension table (e.g., Supplier)
CREATE TABLE dim_supplier (
  supplier_id INT PRIMARY KEY,
  supplier_name VARCHAR(100),
  supplier_address VARCHAR(200),
  -- Other dimension attributes
);

-- Insert data into Swappable Dimension tables
INSERT INTO dim_customer (customer_id, customer_name, customer_address)
VALUES
  (1, 'John Doe', '123 Main St');

INSERT INTO dim_supplier (supplier_id, supplier_name, supplier_address)
VALUES
  (1, 'ABC Corp', '456 Elm St');
  
-- Create relation between Swappable Dimension tables and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_customer
FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id);

ALTER TABLE fact_purchases
ADD CONSTRAINT fk_purchases_supplier
FOREIGN KEY (supplier_id) REFERENCES dim_supplier(supplier_id);

-- Manipulate data in Swappable Dimension tables
UPDATE dim_customer
SET customer_address = '789 Oak Ave'
WHERE customer_id = 1;

UPDATE dim_supplier
SET supplier_address = '890 Pine St'
WHERE supplier_id = 1;
```

Step Dimension:
A step dimension represents a sequence of steps or stages in a process.

```sh
-- Create Step Dimension table
CREATE TABLE dim_process_steps (
  step_id INT PRIMARY KEY,
  step_name VARCHAR(50),
  -- Other dimension attributes
);

-- Insert data into Step Dimension table
INSERT INTO dim_process_steps (step_id, step_name)
VALUES
  (1, 'Step 1'),
  (2, 'Step 2'),
  (3, 'Step 3');
  
-- Create relation between Step Dimension table and Fact table
ALTER TABLE fact_process
ADD CONSTRAINT fk_process_steps
FOREIGN KEY (step_id) REFERENCES dim_process_steps(step_id);

-- Manipulate data in Step Dimension table
UPDATE dim_process_steps
SET step_name = 'New Step'
WHERE step_id = 2;
```

These examples provide a basic understanding of how to create dimensional data models in a Star schema for different types of dimensions. Keep in mind that these are simplified examples, and in real-world scenarios, you may have more complex structures and relationships.


# Snowflake Schema

### Conformed Dimension:
A conformed dimension is a dimension that is shared and consistent across multiple fact tables.
```sh
-- Create Conformed Dimension table
CREATE TABLE dim_customer (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(100),
  customer_address VARCHAR(200),
  -- Other dimension attributes
);

-- Insert data into Conformed Dimension table
INSERT INTO dim_customer (customer_id, customer_name, customer_address)
VALUES
  (1, 'John Doe', '123 Main St'),
  (2, 'Jane Smith', '456 Elm St');
  
-- Create relation between Conformed Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_customer
FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id);

-- Manipulate data in Conformed Dimension table
UPDATE dim_customer
SET customer_address = '789 Oak Ave'
WHERE customer_id = 2;
```

### Outrigger Dimension:
An outrigger dimension is a dimension that is related to another dimension and provides additional attributes.
```sh
-- Create Outrigger Dimension table
CREATE TABLE dim_product_category (
  product_id INT PRIMARY KEY,
  category_id INT,
  category_name VARCHAR(50),
  -- Other dimension attributes
);

-- Insert data into Outrigger Dimension table
INSERT INTO dim_product_category (product_id, category_id, category_name)
VALUES
  (1, 101, 'Electronics'),
  (2, 102, 'Clothing');
  
-- Create relation between Outrigger Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_product_category
FOREIGN KEY (product_id) REFERENCES dim_product_category(product_id);

-- Manipulate data in Outrigger Dimension table
UPDATE dim_product_category
SET category_name = 'Accessories'
WHERE product_id = 2;
```

### Shrunken Dimension:
A shrunken dimension combines multiple low-cardinality dimensions into a single dimension table.
```sh
-- Create Shrunken Dimension table
CREATE TABLE dim_date (
  date_id INT PRIMARY KEY,
  day INT,
  month INT,
  year INT,
  -- Other dimension attributes
);

-- Insert data into Shrunken Dimension table
INSERT INTO dim_date (date_id, day, month, year)
VALUES
  (1, 1, 1, 2023),
  (2, 2, 1, 2023);
  
-- Create relation between Shrunken Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_date
FOREIGN KEY (date_id) REFERENCES dim_date(date_id);

-- Manipulate data in Shrunken Dimension table
UPDATE dim_date
SET year = 2022
WHERE date_id = 2;
```

### Role-Playing Dimension:
A role-playing dimension represents the same dimension table but with different roles or perspectives.
```sh
-- Create Role-Playing Dimension table
CREATE TABLE dim_date (
  date_id INT PRIMARY KEY,
  day INT,
  month INT,
  year INT,
  -- Other dimension attributes
);

-- Insert data into Role-Playing Dimension table
INSERT INTO dim_date (date_id, day, month, year)
VALUES
  (1, 1, 1, 2023),
  (2, 2, 1, 2023);
  
-- Create relation between Role-Playing Dimension and Fact table (e.g., Order Date)
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_order_date
FOREIGN KEY (order_date_id) REFERENCES dim_date(date_id);

-- Create relation betweenRole-Playing Dimension and Fact table (e.g., Ship Date)
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_ship_date
FOREIGN KEY (ship_date_id) REFERENCES dim_date(date_id);

-- Manipulate data in Role-Playing Dimension table
UPDATE dim_date
SET year = 2022
WHERE date_id = 2;
```

### Dimension to Dimension Table:
A dimension to dimension table represents a hierarchical relationship between dimensions.
```sh
-- Create Dimension to Dimension Table
CREATE TABLE dim_product_hierarchy (
  product_id INT PRIMARY KEY,
  parent_product_id INT,
  product_name VARCHAR(100),
  -- Other dimension attributes
);

-- Insert data into Dimension to Dimension Table
INSERT INTO dim_product_hierarchy (product_id, parent_product_id, product_name)
VALUES
  (1, NULL, 'Electronics'),
  (2, 1, 'Smartphones'),
  (3, 1, 'Laptops');
  
-- Create relation between Dimension to Dimension Table and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_product_hierarchy
FOREIGN KEY (product_id) REFERENCES dim_product_hierarchy(product_id);

-- Manipulate data in Dimension to Dimension Table
UPDATE dim_product_hierarchy
SET product_name = 'Mobile Phones'
WHERE product_id = 2;
```

### Junk Dimension:
A junk dimension combines multiple low-cardinality flags or indicators into a single dimension table.
```sh
-- Create Junk Dimension table
CREATE TABLE dim_flags (
  flag_id INT PRIMARY KEY,
  is_active BOOLEAN,
  is_promotion BOOLEAN,
  -- Other flag attributes
);

-- Insert data into Junk Dimension table
INSERT INTO dim_flags (flag_id, is_active, is_promotion)
VALUES
  (1, TRUE, FALSE),
  (2, TRUE, TRUE);
  
-- Create relation between Junk Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_flags
FOREIGN KEY (flag_id) REFERENCES dim_flags(flag_id);

-- Manipulate data in Junk Dimension table
UPDATE dim_flags
SET is_promotion = TRUE
WHERE flag_id = 2;
```

### Degenerate Dimension:
A degenerate dimension represents a dimension attribute that exists only in the fact table.
```sh
-- Create Fact table with Degenerate Dimension
CREATE TABLE fact_sales (
  sale_id INT PRIMARY KEY,
  product_id INT,
  quantity INT,
  -- Other fact attributes
  order_number VARCHAR(20) -- Degenerate dimension
);

-- Insert data into Fact table
INSERT INTO fact_sales (sale_id, product_id, quantity, order_number)
VALUES
  (1, 101, 5, 'ORD001'),
  (2, 102, 3, 'ORD002');
  
-- Manipulate data in Fact table with Degenerate Dimension
UPDATE fact_sales
SET order_number = 'ORD003'
WHERE sale_id = 2;
```

### Swappable Dimension:
A swappable dimension allows for multiple dimension tables to be used interchangeably.
```sh
-- Create Swappable Dimension table (e.g., Customer)
CREATE TABLE dim_customer (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(100),
  customer_address VARCHAR(200),
  -- Other dimension attributes
);

-- Create Swappable Dimension table (e.g., Supplier)
CREATE TABLE dim_supplier (
  supplier_id INT PRIMARY KEY,
  supplier_name VARCHAR(100),
  supplier_address VARCHAR(200),
  -- Other dimension attributes
);

-- Insert data into Swappable Dimension tables
INSERT INTO dim_customer (customer_id, customer_name, customer_address)
VALUES
  (1, 'John Doe', '123 Main St');

INSERT INTO dim_supplier (supplier_id, supplier_name, supplier_address)
VALUES
  (1, 'ABC Corp', '456Elm St');
  
-- Create relation between Swappable Dimension tables and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_customer
FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id);

ALTER TABLE fact_purchases
ADD CONSTRAINT fk_purchases_supplier
FOREIGN KEY (supplier_id) REFERENCES dim_supplier(supplier_id);

-- Manipulate data in Swappable Dimension tables
UPDATE dim_customer
SET customer_address = '789 Oak Ave'
WHERE customer_id = 1;

UPDATE dim_supplier
SET supplier_address = '890 Pine St'
WHERE supplier_id = 1;
```

### Step Dimension:
A step dimension represents a sequence of steps or stages in a process.
```sh
-- Create Step Dimension table
CREATE TABLE dim_process_steps (
  step_id INT PRIMARY KEY,
  step_name VARCHAR(50),
  -- Other dimension attributes
);

-- Insert data into Step Dimension table
INSERT INTO dim_process_steps (step_id, step_name)
VALUES
  (1, 'Step 1'),
  (2, 'Step 2'),
  (3, 'Step 3');
  
-- Create relation between Step Dimension table and Fact table
ALTER TABLE fact_process
ADD CONSTRAINT fk_process_steps
FOREIGN KEY (step_id) REFERENCES dim_process_steps(step_id);

-- Manipulate data in Step Dimension table
UPDATE dim_process_steps
SET step_name = 'New Step'
WHERE step_id = 2;
```

These examples provide a basic understanding of how to create dimensional data models in a Snowflake schema for different types of dimensions. Keep in mind that these are simplified examples, and in real-world scenarios, you may have more complex structures and relationships.

# Galaxy Schema

### Conformed Dimension:
A conformed dimension is a dimension that is shared and consistent across multiple fact tables.
```sh
-- Create Conformed Dimension table
CREATE TABLE dim_customer (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(100),
  customer_address VARCHAR(200),
  -- Other dimension attributes
);

-- Insert data into Conformed Dimension table
INSERT INTO dim_customer (customer_id, customer_name, customer_address)
VALUES
  (1, 'John Doe', '123 Main St'),
  (2, 'Jane Smith', '456 Elm St');
  
-- Create relation between Conformed Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_customer
FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id);

-- Manipulate data in Conformed Dimension table
UPDATE dim_customer
SET customer_address = '789 Oak Ave'
WHERE customer_id = 2;
```

### Outrigger Dimension:
An outrigger dimension is a dimension that is related to another dimension and provides additional attributes.
```sh
-- Create Outrigger Dimension table
CREATE TABLE dim_product_category (
  product_id INT PRIMARY KEY,
  category_id INT,
  category_name VARCHAR(50),
  -- Other dimension attributes
);

-- Insert data into Outrigger Dimension table
INSERT INTO dim_product_category (product_id, category_id, category_name)
VALUES
  (1, 101, 'Electronics'),
  (2, 102, 'Clothing');
  
-- Create relation between Outrigger Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_product_category
FOREIGN KEY (product_id) REFERENCES dim_product_category(product_id);

-- Manipulate data in Outrigger Dimension table
UPDATE dim_product_category
SET category_name = 'Accessories'
WHERE product_id = 2;
```

### Shrunken Dimension:
A shrunken dimension combines multiple low-cardinality dimensions into a single dimension table.
```sh
-- Create Shrunken Dimension table
CREATE TABLE dim_date (
  date_id INT PRIMARY KEY,
  day INT,
  month INT,
  year INT,
  -- Other dimension attributes
);

-- Insert data into Shrunken Dimension table
INSERT INTO dim_date (date_id, day, month, year)
VALUES
  (1, 1, 1, 2023),
  (2, 2, 1, 2023);
  
-- Create relation between Shrunken Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_date
FOREIGN KEY (date_id) REFERENCES dim_date(date_id);

-- Manipulate data in Shrunken Dimension table
UPDATE dim_date
SET year = 2022
WHERE date_id = 2;
```

### Role-Playing Dimension:
A role-playing dimension represents the same dimension table but with different roles or perspectives.
```sh
-- Create Role-Playing Dimension table
CREATE TABLE dim_date (
  date_id INT PRIMARY KEY,
  day INT,
  month INT,
  year INT,
  -- Other dimension attributes
);

-- Insert data into Role-Playing Dimension table
INSERT INTO dim_date (date_id, day, month, year)
VALUES
  (1, 1, 1, 2023),
  (2, 2, 1, 2023);
  
-- Create relation between Role-Playing Dimension and Fact table (e.g., Order Date)
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_order_date
FOREIGN KEY (order_date_id) REFERENCES dim_date(date_id);

-- Create relation between Role-Playing Dimension and Fact table (e.g., Ship Date)
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_ship_date
FOREIGN KEY (ship_date_id) REFERENCES dim_date(date_id);

-- Manipulate data in Role-Playing Dimension table
UPDATE dim_date
SET year = 2022
WHERE date_id = 2;
```

### Dimension to Dimension Table:
A dimension to dimension table represents a hierarchical relationship between dimensions.
```sh
-- Create Dimension to Dimension Table
CREATE TABLE dim_product_hierarchy (
  product_id INT PRIMARY KEY,
  parent_product_id INT,
  product_name VARCHAR(100),
  -- Other dimension attributes
);

-- Insert data into Dimension to Dimension Table
INSERT INTO dim_product_hierarchy (product_id, parent_product_id, product_name)
VALUES
  (1, NULL, 'Electronics'),
  (2, 1, 'Smartphones'),
  (3, 1, 'Laptops');
  
-- Create relation between Dimension to Dimension Table and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_product_hierarchy
FOREIGN KEY (product_id) REFERENCES dim_product_hierarchy(product_id);

-- Manipulate data in Dimension to Dimension Table
UPDATE dim_product_hierarchy
SET product_name = 'Mobile Phones'
WHERE product_id = 2;
```

### Junk Dimension:
A junk dimension combines multiple low-cardinality flags or indicators into a single dimension table.
```sh
-- Create Junk Dimension table
CREATE TABLE dim_flags (
  flag_id INT PRIMARY KEY,
  is_active BOOLEAN,
  is_promotion BOOLEAN,
  -- Other flag attributes
);

-- Insert data into Junk Dimension table
INSERT INTO dim_flags (flag_id, is_active, is_promotion)
VALUES
  (1, TRUE, FALSE),
  (2, TRUE, TRUE);
  
-- Create relation between Junk Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_flags
FOREIGN KEY (flag_id) REFERENCES dim_flags(flag_id);

-- Manipulate data in Junk Dimension table
UPDATE dim_flags
SET is_promotion = TRUE
WHERE flag_id = 2;
```

### Degenerate Dimension:
A degenerate dimension represents a dimension attribute that exists only in the fact table.
```sh
-- Create Fact table with Degenerate Dimension
CREATE TABLE fact_sales (
  sale_id INT PRIMARY KEY,
  product_id INT,
  quantity INT,
  -- Other fact attributes
  order_number VARCHAR(20) -- Degenerate dimension
);

-- Insert data into Fact table
INSERT INTO fact_sales (sale_id, product_id, quantity, order_number)
VALUES
  (1, 101, 5, 'ORD001'),
  (2, 102, 3, 'ORD002');
  
-- Manipulate data in Fact table with Degenerate Dimension
UPDATE fact_sales
SET order_number = 'ORD003'
WHERE sale_id = 2;
```

### Swappable Dimension:
A swappable dimension allows for multiple dimension tables to be used interchangeably.
```sh
-- Create Swappable Dimension table (e.g., Customer)
CREATE TABLE dim_customer (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(100),
  customer_address VARCHAR(200),
  -- Other dimension attributes
);

-- Create Swappable Dimension table (e.g., Supplier)
CREATE TABLE dim_supplier (
  supplier_id INT PRIMARY KEY,
  supplier_name VARCHAR(100),
  supplier_address VARCHAR(200),
  -- Other dimension attributes
);

-- Insert data into Swappable Dimension tables
INSERT INTO dim_customer (customer_id, customer_name, customer_address)
VALUES
  (1, 'John Doe', '123 Main St');

INSERT INTO dim_supplier (supplier_id, supplier_name, supplier_address)
VALUES
  (1, 'ABC Corp', '456 ElmSt');
  
-- Create relation between Swappable Dimension tables and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_customer
FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id);

ALTER TABLE fact_purchases
ADD CONSTRAINT fk_purchases_supplier
FOREIGN KEY (supplier_id) REFERENCES dim_supplier(supplier_id);

-- Manipulate data in Swappable Dimension tables
UPDATE dim_customer
SET customer_address = '789 Oak Ave'
WHERE customer_id = 1;

UPDATE dim_supplier
SET supplier_address = '890 Pine St'
WHERE supplier_id = 1;
```

### Step Dimension:
A step dimension represents a sequence of steps or stages in a process.
```sh
-- Create Step Dimension table
CREATE TABLE dim_process_steps (
  step_id INT PRIMARY KEY,
  step_name VARCHAR(50),
  -- Other dimension attributes
);

-- Insert data into Step Dimension table
INSERT INTO dim_process_steps (step_id, step_name)
VALUES
  (1, 'Step 1'),
  (2, 'Step 2'),
  (3, 'Step 3');
  
-- Create relation between Step Dimension table and Fact table
ALTER TABLE fact_process
ADD CONSTRAINT fk_process_steps
FOREIGN KEY (step_id) REFERENCES dim_process_steps(step_id);

-- Manipulate data in Step Dimension table
UPDATE dim_process_steps
SET step_name = 'New Step'
WHERE step_id = 2;
```

These examples provide a basic understanding of how to create dimensional data models in a Galaxy schema for different types of dimensions. Keep in mind that these are simplified examples, and in real-world scenarios, you may have more complex structures and relationships.

# Fact Constellation Schema

### Conformed Dimension:
A conformed dimension is a dimension that is shared and consistent across multiple fact tables.
```sh
-- Create Conformed Dimension table
CREATE TABLE dim_customer (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(100),
  customer_address VARCHAR(200),
  -- Other dimension attributes
);

-- Insert data into Conformed Dimension table
INSERT INTO dim_customer (customer_id, customer_name, customer_address)
VALUES
  (1, 'John Doe', '123 Main St'),
  (2, 'Jane Smith', '456 Elm St');
  
-- Create relation between Conformed Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_customer
FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id);

-- Manipulate data in Conformed Dimension table
UPDATE dim_customer
SET customer_address = '789 Oak Ave'
WHERE customer_id = 2;
```

### Outrigger Dimension:
An outrigger dimension is a dimension that is related to another dimension and provides additional attributes.
```sh
-- Create Outrigger Dimension table
CREATE TABLE dim_product_category (
  product_id INT PRIMARY KEY,
  category_id INT,
  category_name VARCHAR(50),
  -- Other dimension attributes
);

-- Insert data into Outrigger Dimension table
INSERT INTO dim_product_category (product_id, category_id, category_name)
VALUES
  (1, 101, 'Electronics'),
  (2, 102, 'Clothing');
  
-- Create relation between Outrigger Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_product_category
FOREIGN KEY (product_id) REFERENCES dim_product_category(product_id);

-- Manipulate data in Outrigger Dimension table
UPDATE dim_product_category
SET category_name = 'Accessories'
WHERE product_id = 2;
```

### Shrunken Dimension:
A shrunken dimension combines multiple low-cardinality dimensions into a single dimension table.
```sh
-- Create Shrunken Dimension table
CREATE TABLE dim_date (
  date_id INT PRIMARY KEY,
  day INT,
  month INT,
  year INT,
  -- Other dimension attributes
);

-- Insert data into Shrunken Dimension table
INSERT INTO dim_date (date_id, day, month, year)
VALUES
  (1, 1, 1, 2023),
  (2, 2, 1, 2023);
  
-- Create relation between Shrunken Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_date
FOREIGN KEY (date_id) REFERENCES dim_date(date_id);

-- Manipulate data in Shrunken Dimension table
UPDATE dim_date
SET year = 2022
WHERE date_id = 2;
```

### Role-Playing Dimension:
A role-playing dimension represents the same dimension table but with different roles or perspectives.
```sh
-- Create Role-Playing Dimension table
CREATE TABLE dim_date (
  date_id INT PRIMARY KEY,
  day INT,
  month INT,
  year INT,
  -- Other dimension attributes
);

-- Insert data into Role-Playing Dimension table
INSERT INTO dim_date (date_id, day, month, year)
VALUES
  (1, 1, 1, 2023),
  (2, 2, 1, 2023);
  
-- Create relation between Role-Playing Dimension and Fact table (e.g., Order Date)
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_order_date
FOREIGN KEY (order_date_id) REFERENCES dim_date(date_id);

-- Create relationbetween Role-Playing Dimension and Fact table (e.g., Ship Date)
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_ship_date
FOREIGN KEY (ship_date_id) REFERENCES dim_date(date_id);

-- Manipulate data in Role-Playing Dimension table
UPDATE dim_date
SET year = 2022
WHERE date_id = 2;
```
### Dimension to Dimension Table:
A dimension to dimension table represents a hierarchical relationship between dimensions.
```sh
-- Create Dimension to Dimension Table
CREATE TABLE dim_product_hierarchy (
  product_id INT PRIMARY KEY,
  parent_product_id INT,
  product_name VARCHAR(100),
  -- Other dimension attributes
);

-- Insert data into Dimension to Dimension Table
INSERT INTO dim_product_hierarchy (product_id, parent_product_id, product_name)
VALUES
  (1, NULL, 'Electronics'),
  (2, 1, 'Smartphones'),
  (3, 1, 'Laptops');
  
-- Create relation between Dimension to Dimension Table and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_product_hierarchy
FOREIGN KEY (product_id) REFERENCES dim_product_hierarchy(product_id);

-- Manipulate data in Dimension to Dimension Table
UPDATE dim_product_hierarchy
SET product_name = 'Mobile Phones'
WHERE product_id = 2;
```

### Junk Dimension:
A junk dimension combines multiple low-cardinality flags or indicators into a single dimension table.
```sh
-- Create Junk Dimension table
CREATE TABLE dim_flags (
  flag_id INT PRIMARY KEY,
  is_active BOOLEAN,
  is_promotion BOOLEAN,
  -- Other flag attributes
);

-- Insert data into Junk Dimension table
INSERT INTO dim_flags (flag_id, is_active, is_promotion)
VALUES
  (1, TRUE, FALSE),
  (2, TRUE, TRUE);
  
-- Create relation between Junk Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_flags
FOREIGN KEY (flag_id) REFERENCES dim_flags(flag_id);

-- Manipulate data in Junk Dimension table
UPDATE dim_flags
SET is_promotion = TRUE
WHERE flag_id = 2;
```

### Degenerate Dimension:
A degenerate dimension represents a dimension attribute that exists only in the fact table.
```sh
-- Create Fact table with Degenerate Dimension
CREATE TABLE fact_sales (
  sale_id INT PRIMARY KEY,
  product_id INT,
  quantity INT,
  -- Other fact attributes
  order_number VARCHAR(20) -- Degenerate dimension
);

-- Insert data into Fact table
INSERT INTO fact_sales (sale_id, product_id, quantity, order_number)
VALUES
  (1, 101, 5, 'ORD001'),
  (2, 102, 3, 'ORD002');
  
-- Manipulate data in Fact table with Degenerate Dimension
UPDATE fact_sales
SET order_number = 'ORD003'
WHERE sale_id = 2;
```

### Swappable Dimension:
A swappable dimension allows for multiple dimension tables to be used interchangeably.
```sh
-- Create Swappable Dimension table (e.g., Customer)
CREATE TABLE dim_customer (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(100),
  customer_address VARCHAR(200),
  -- Other dimension attributes
);

-- Create Swappable Dimension table (e.g., Supplier)
CREATE TABLE dim_supplier (
  supplier_id INT PRIMARY KEY,
  supplier_name VARCHAR(100),
  supplier_address VARCHAR(200),
  -- Other dimension attributes
);

-- Insert data into Swappable Dimension tables
INSERT INTO dim_customer (customer_id, customer_name, customer_address)
VALUES
  (1, 'John Doe', '123 Main St');

INSERT INTO dim_supplier (supplier_id, supplier_name, supplier_address)
VALUES
  (1, 'ABC Corp', '456 Elm St');
  
-- Create relation between Swappable Dimension tables and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_customer
FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id);

ALTER TABLE fact_purchases
ADD CONSTRAINT fk_purchases_supplier
FOREIGN KEY (supplier_id) REFERENCES dim_supplier(supplier_id);

-- Manipulate data in Swappable Dimension tables
UPDATE dim_customer
SET customer_address = '789 Oak Ave'
WHERE customer_id = 1;

UPDATE dim_supplier
SET supplier_address = '890 Pine St'
WHERE supplier_id = 1;
```

### Step Dimension:
A step dimension represents a sequence of steps or stages in a process.
```sh
-- Create Step Dimension table
CREATE TABLE dim_process_steps (
  step_id INT PRIMARY KEY,
  step_name VARCHAR(50),
  -- Other dimension attributes
);

-- Insert data into Step Dimension table
INSERT INTO dim_process_steps (step_id, step_name)
VALUES
  (1, 'Step 1'),
  (2, 'Step 2'),
  (3, 'Step 3');
  
-- Create relation between Step Dimension table and Fact table
ALTER TABLE fact_process
ADD CONSTRAINT fk_process_steps
FOREIGN KEY (step_id) REFERENCES dim_process_steps(step_id);

-- Manipulate data in Step Dimension table
UPDATE dim_process_steps
SET step_name = 'New Step'
WHERE step_id = 2;
```

These examples provide a basic understanding of how to create dimensional data models in a Fact Constellation schema for different types of dimensions. Keep in mind that these are simplified examples, and in real-world scenarios, you may have more complex structures and relationships.


# Star Cluster Schema

### Conformed Dimension:
A conformed dimension is a dimension that is shared and consistent across multiple fact tables.
```sh
-- Create Conformed Dimension table
CREATE TABLE dim_customer (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(100),
  customer_address VARCHAR(200),
  -- Other dimension attributes
);

-- Insert data into Conformed Dimension table
INSERT INTO dim_customer (customer_id, customer_name, customer_address)
VALUES
  (1, 'John Doe', '123 Main St'),
  (2, 'Jane Smith', '456 Elm St');
  
-- Create relation between Conformed Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_customer
FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id);

-- Manipulate data in Conformed Dimension table
UPDATE dim_customer
SET customer_address = '789 Oak Ave'
WHERE customer_id = 2;
```

### Outrigger Dimension:
An outrigger dimension is a dimension that is related to another dimension and provides additional attributes.
```sh
-- Create Outrigger Dimension table
CREATE TABLE dim_product_category (
  product_id INT PRIMARY KEY,
  category_id INT,
  category_name VARCHAR(50),
  -- Other dimension attributes
);

-- Insert data into Outrigger Dimension table
INSERT INTO dim_product_category (product_id, category_id, category_name)
VALUES
  (1, 101, 'Electronics'),
  (2, 102, 'Clothing');
  
-- Create relation between Outrigger Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_product_category
FOREIGN KEY (product_id) REFERENCES dim_product_category(product_id);

-- Manipulate data in Outrigger Dimension table
UPDATE dim_product_category
SET category_name = 'Accessories'
WHERE product_id = 2;
```

### Shrunken Dimension:
A shrunken dimension combines multiple low-cardinality dimensions into a single dimension table.
```sh
-- Create Shrunken Dimension table
CREATE TABLE dim_date (
  date_id INT PRIMARY KEY,
  day INT,
  month INT,
  year INT,
  -- Other dimension attributes
);

-- Insert data into Shrunken Dimension table
INSERT INTO dim_date (date_id, day, month, year)
VALUES
  (1, 1, 1, 2023),
  (2, 2, 1, 2023);
  
-- Create relation between Shrunken Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_date
FOREIGN KEY (date_id) REFERENCES dim_date(date_id);

-- Manipulate data in Shrunken Dimension table
UPDATE dim_date
SET year = 2022
WHERE date_id = 2;
```

### Role-Playing Dimension:
A role-playing dimension represents the same dimension table but with different roles or perspectives.
```sh
-- Create Role-Playing Dimension table
CREATE TABLE dim_date (
  date_id INT PRIMARY KEY,
  day INT,
  month INT,
  year INT,
  -- Other dimension attributes
);

-- Insert data into Role-Playing Dimension table
INSERT INTO dim_date (date_id, day, month, year)
VALUES
  (1, 1, 1, 2023),
  (2, 2, 1, 2023);
  
-- Create relation between Role-Playing Dimension and Fact table (e.g., Order Date)
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_order_date
FOREIGN KEY (order_date_id) REFERENCES dim_date(date_id);

-- Create relation betweenRole-Playing Dimension and Fact table (e.g., Ship Date)
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_ship_date
FOREIGN KEY (ship_date_id) REFERENCES dim_date(date_id);

-- Manipulate data in Role-Playing Dimension table
UPDATE dim_date
SET year = 2022
WHERE date_id = 2;
```

### Dimension to Dimension Table:
A dimension to dimension table represents a hierarchical relationship between dimensions.
```sh
-- Create Dimension to Dimension Table
CREATE TABLE dim_product_hierarchy (
  product_id INT PRIMARY KEY,
  parent_product_id INT,
  product_name VARCHAR(100),
  -- Other dimension attributes
);

-- Insert data into Dimension to Dimension Table
INSERT INTO dim_product_hierarchy (product_id, parent_product_id, product_name)
VALUES
  (1, NULL, 'Electronics'),
  (2, 1, 'Smartphones'),
  (3, 1, 'Laptops');
  
-- Create relation between Dimension to Dimension Table and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_product_hierarchy
FOREIGN KEY (product_id) REFERENCES dim_product_hierarchy(product_id);

-- Manipulate data in Dimension to Dimension Table
UPDATE dim_product_hierarchy
SET product_name = 'Mobile Phones'
WHERE product_id = 2;
```

### Junk Dimension:
A junk dimension combines multiple low-cardinality flags or indicators into a single dimension table.
```sh
-- Create Junk Dimension table
CREATE TABLE dim_flags (
  flag_id INT PRIMARY KEY,
  is_active BOOLEAN,
  is_promotion BOOLEAN,
  -- Other flag attributes
);

-- Insert data into Junk Dimension table
INSERT INTO dim_flags (flag_id, is_active, is_promotion)
VALUES
  (1, TRUE, FALSE),
  (2, TRUE, TRUE);
  
-- Create relation between Junk Dimension and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_flags
FOREIGN KEY (flag_id) REFERENCES dim_flags(flag_id);

-- Manipulate data in Junk Dimension table
UPDATE dim_flags
SET is_promotion = TRUE
WHERE flag_id = 2;
```

### Degenerate Dimension:
A degenerate dimension represents a dimension attribute that exists only in the fact table.
```sh
-- Create Fact table with Degenerate Dimension
CREATE TABLE fact_sales (
  sale_id INT PRIMARY KEY,
  product_id INT,
  quantity INT,
  -- Other fact attributes
  order_number VARCHAR(20) -- Degenerate dimension
);

-- Insert data into Fact table
INSERT INTO fact_sales (sale_id, product_id, quantity, order_number)
VALUES
  (1, 101, 5, 'ORD001'),
  (2, 102, 3, 'ORD002');
  
-- Manipulate data in Fact table with Degenerate Dimension
UPDATE fact_sales
SET order_number = 'ORD003'
WHERE sale_id = 2;
```

Swappable Dimension:
A swappable dimension allows for multiple dimension tables to be used interchangeably.
```sh
-- Create Swappable Dimension table (e.g., Customer)
CREATE TABLE dim_customer (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(100),
  customer_address VARCHAR(200),
  -- Other dimension attributes
);

-- Create Swappable Dimension table (e.g., Supplier)
CREATE TABLE dim_supplier (
  supplier_id INT PRIMARY KEY,
  supplier_name VARCHAR(100),
  supplier_address VARCHAR(200),
  -- Other dimension attributes
);

-- Insert data into Swappable Dimension tables
INSERT INTO dim_customer (customer_id, customer_name, customer_address)
VALUES
  (1, 'John Doe', '123 Main St');

INSERT INTO dim_supplier (supplier_id, supplier_name, supplier_address)
VALUES
  (1, 'ABC Corp', '456Elm St');
  
-- Create relation between Swappable Dimension tables and Fact table
ALTER TABLE fact_sales
ADD CONSTRAINT fk_sales_customer
FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id);

ALTER TABLE fact_purchases
ADD CONSTRAINT fk_purchases_supplier
FOREIGN KEY (supplier_id) REFERENCES dim_supplier(supplier_id);

-- Manipulate data in Swappable Dimension tables
UPDATE dim_customer
SET customer_address = '789 Oak Ave'
WHERE customer_id = 1;

UPDATE dim_supplier
SET supplier_address = '890 Pine St'
WHERE supplier_id = 1;
```

### Step Dimension:
A step dimension represents a sequence of steps or stages in a process.
```sh
-- Create Step Dimension table
CREATE TABLE dim_process_steps (
  step_id INT PRIMARY KEY,
  step_name VARCHAR(50),
  -- Other dimension attributes
);

-- Insert data into Step Dimension table
INSERT INTO dim_process_steps (step_id, step_name)
VALUES
  (1, 'Step 1'),
  (2, 'Step 2'),
  (3, 'Step 3');
  
-- Create relation between Step Dimension table and Fact table
ALTER TABLE fact_process
ADD CONSTRAINT fk_process_steps
FOREIGN KEY (step_id) REFERENCES dim_process_steps(step_id);

-- Manipulate data in Step Dimension table
UPDATE dim_process_steps
SET step_name = 'New Step'
WHERE step_id = 2;
```

These examples provide a basic understanding of how to create dimensional data models in a Star Cluster schema for different types of dimensions. Keep in mind that these are simplified examples, and in real-world scenarios, you may have more complex structures and relationships.