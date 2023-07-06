# DBT

![DBT](https://www.getdbt.com/ui/img/png/analytics-engineering-dbt.png)  

DBT is a framework used for high-level SQL transformation logic. Data engineers use dbt to transform and model data in a data warehouse. It is an essential tool used in data modeling to build the data model into smaller modules. With dbt, you can modularize data transformation logic into discrete dbt models. It enables you to reuse the dbt models for different use cases to enhance productivity and collaboration. dbt data modeling is also beneficial for testing and debugging data models.

- [DBT](https://www.getdbt.com/)
- [Install DBT Core in local](https://docs.getdbt.com/docs/core/installation)
- [BigQuery configurations](https://docs.getdbt.com/reference/resource-configs/bigquery-configs)
- [DBT Cloud & BigQuery](https://docs.getdbt.com/quickstarts/bigquery?step=15)

### Implementing Data Modeling with dbt
Data modeling with dbt is a way of transforming data for business intelligence or downstream applications in a modular approach. The transformation logic is built through dbt models consisting of SQL SELECT statements. 

These models can then be referenced by other models to obtain modularity in your dbt projects. dbt also includes dbt sources which are metadata for the raw data. 

Using sources, you can reference the underlying data to build transformation in dbt models. The data defined in the dbt sources can be referenced in the dbt models using the source function. The approach of referencing transformation logic and data sources in every step of the dbt workflows makes it a good fit for data modeling.

The ability to include test cases to establish data quality and integrity while building a dbt project further helps in data modeling. Tests are SQL expression that validates models, sources, and other checkpoints. 

To start with dbt data modeling, you need to know the data source, what you want to create (views or tables), testing requirements, and more. 

In a dbt project, there are two core files: <b>.config</b> and <b>.sql</b>. The <b>.config</b> files define sources, configure paths, and set versions. It informs dbt how the data models can be built in the target environment. 

<b>.sql</b> files are used to define your data models. It consists of a configuration block that uses Jinja, common table expressions, and other temporary tables. <b>.sql</b> files also contain a final <b>select</b> statement that gives you the transformed data.

Consider the following command:

<b>select * from {{ ref(‘stg_customers’) }}</b>

The double curly brackets in the aforementioned command are jinja syntax that tells dbt to reference another dataset within its data source. In this case, it is <b>‘stg_customers.’</b>

