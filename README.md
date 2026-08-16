# Retail Data Platform

A Python-based ETL pipeline that extracts retail sales data from CSV files, performs data transformation and quality validation using Pandas, and loads the processed data into PostgreSQL.

## Project Overview

This project demonstrates an end-to-end batch ETL pipeline for processing retail sales data.

The pipeline:

1. Extracts raw sales data from a CSV file.
2. Transforms and validates the data using Python and Pandas.
3. Loads the processed data into PostgreSQL.
4. Uses logging and error handling to monitor pipeline execution.
5. Handles duplicate orders using PostgreSQL upsert logic.

## Architecture

```text
CSV File
   |
   v
extract.py
   |
   v
Pandas DataFrame
   |
   v
transform.py
   |
   |-- Calculate total amount
   |-- Convert order date
   |-- Validate missing values
   |-- Validate quantity and price
   |-- Check duplicate order IDs
   |
   v
load.py
   |
   v
PostgreSQL
   |
   v
sales table
```

## Technologies Used

* Python
* Pandas
* PostgreSQL
* SQLAlchemy
* psycopg2
* python-dotenv
* Git / GitHub

## Project Structure

```text
Retail-data-platform/
|
|-- config/
|-- data/
|   `-- raw/
|       `-- sales_data.csv
|
|-- docs/
|-- logs/
|-- sql/
|
|-- src/
|   |-- extract.py
|   |-- transform.py
|   |-- load.py
|   `-- main.py
|
|-- tests/
|-- .gitignore
|-- README.md
`-- requirements.txt
```

Database credentials are stored locally in a `.env` file inside the `src` directory. The `.env` file is excluded from Git using `.gitignore`.

## ETL Pipeline

### 1. Extract

`extract.py` reads the raw CSV file using Pandas and returns the data as a DataFrame.

The pipeline also logs the number of records extracted.

Example:

```text
Extracted 3 rows from CSV
```

### 2. Transform and Validate

`transform.py` performs data transformation and quality checks.

#### Transformations

* Calculates `total_amount` using:

```text
total_amount = quantity * price
```

* Converts `order_date` into a datetime format.

#### Data Quality Checks

* Detects missing values.
* Validates that quantity is greater than zero.
* Validates that price is greater than zero.
* Detects duplicate `order_id` values.

Validation failures for quantity, price, and duplicate order IDs stop the pipeline from loading invalid data, while missing values are logged as warnings.

### 3. Load

`load.py` loads the transformed data into PostgreSQL using SQLAlchemy and psycopg2.

The data is loaded into the `sales` table.

The pipeline uses PostgreSQL `ON CONFLICT` logic on `order_id` to update an existing order instead of creating a duplicate record.

Database operations are executed inside a transaction using SQLAlchemy.

## Database Schema

The `sales` table contains:

| Column         | Description               |
| -------------- | ------------------------- |
| `order_id`     | Unique order identifier   |
| `order_date`   | Date of the order         |
| `customer_id`  | Customer identifier       |
| `product`      | Product purchased         |
| `category`     | Product category          |
| `quantity`     | Number of units purchased |
| `price`        | Price per unit            |
| `total_amount` | Calculated order amount   |

## Sample Data

The current sample dataset contains three retail transactions:

| Order ID | Product  | Quantity | Price | Total Amount |
| -------: | -------- | -------: | ----: | -----------: |
|     1001 | Laptop   |        1 | 75000 |        75000 |
|     1002 | Mouse    |        2 |  1200 |         2400 |
|     1003 | Keyboard |        1 |  2500 |         2500 |

Total sales value in the sample dataset: **INR 79,900**

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/anushav-12/Retail-data-platform.git
cd Retail-data-platform
```

### 2. Create and activate a virtual environment

On Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure database credentials

Create a `.env` file inside the `src` directory:

```text
DB_PASSWORD=your_postgresql_password
```

The `.env` file is excluded from Git using `.gitignore`.

### 5. Configure PostgreSQL

Create the `retail_pipeline` database and the required `sales` table.

### 6. Run the pipeline

From the project root:

```powershell
cd src
python main.py
```

## Sample Pipeline Output

```text
ETL pipeline started
Extracted 3 rows from CSV
Transformation and validation completed successfully
Loaded 3 rows into PostgreSQL
ETL pipeline completed successfully
```

The loaded records were verified in PostgreSQL using pgAdmin.

## Error Handling and Logging

The pipeline includes:

* Exception handling during extraction, transformation, and loading.
* Informative logging for pipeline execution.
* Data validation failures.
* Database transaction handling.
* PostgreSQL conflict handling for duplicate order IDs.

## Future Enhancements

Planned improvements for future phases include:

* Batch/bulk database loading for larger datasets.
* Automated pipeline scheduling with Apache Airflow.
* Docker containerization.
* Cloud data warehouse integration.
* Incremental data processing.
* Additional automated data-quality tests.
* Scalable processing using distributed data technologies.

## Project Status

**Phase 1 - Completed**

Current implementation:

**CSV -> Python/Pandas ETL -> PostgreSQL**

Future phases will focus on orchestration, containerization, scalability, and cloud integration.
