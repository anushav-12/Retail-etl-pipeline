# Retail Sales ETL Pipeline

A Python-based batch ETL pipeline that extracts retail sales data from CSV files, performs data transformation and quality validation using Pandas, and loads the processed data into PostgreSQL with idempotent, batched upserts.

## Project Overview

This project demonstrates an end-to-end batch ETL pipeline for processing retail sales data at realistic volume (50,000+ records).

The pipeline:

1. Extracts raw sales data from a CSV file.
2. Transforms and validates the data using Python and Pandas.
3. Quarantines invalid records (with reasons logged) instead of failing the entire batch.
4. Loads the processed data into PostgreSQL using batched upserts.
5. Uses logging and error handling to monitor pipeline execution end-to-end.

## Architecture

```text
CSV File (50k+ rows)
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
   |-- Flag missing values
   |-- Quarantine invalid quantity / price / duplicate order_id
   |-- Write quarantined rows to data/processed/quarantined_rows.csv
   |
   v
Clean DataFrame
   |
   v
load.py
   |
   |-- Batched upsert (5,000 rows/batch) via SQLAlchemy
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
* Faker (synthetic test data generation)
* pytest (unit testing)
* Git / GitHub

## Project Structure

```text
Retail-data-platform/
|
|-- config/
|-- data/
|   |-- processed/
|   |   `-- quarantined_rows.csv   (generated at runtime)
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
|   `-- test_transform.py
|
|-- generate_data.py
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
Extracted 50000 rows from CSV
```

### 2. Transform and Validate

`transform.py` performs data transformation and **row-level quality validation with quarantining** — invalid rows are set aside rather than blocking the entire batch.

#### Transformations

* Calculates `total_amount` using:

```text
total_amount = quantity * price
```

* Converts `order_date` into a datetime format.

#### Data Quality Checks (quarantine, not hard failure)

* Missing values are detected and logged as warnings.
* Rows with `quantity <= 0` are quarantined.
* Rows with missing or non-positive `price` are quarantined.
* Duplicate `order_id` values are quarantined (first occurrence kept).
* Quarantined rows are written to `data/processed/quarantined_rows.csv` for audit.
* If **all** rows fail validation, the pipeline raises an error and halts — treated as a structural data problem rather than a normal data quality issue.

On a representative 50,000-row synthetic run: 2,267 rows were quarantined (1,036 invalid quantity, 506 missing price, 768 duplicate order IDs), while 47,733 valid rows proceeded to load.

### 3. Load

`load.py` loads the transformed data into PostgreSQL using SQLAlchemy and psycopg2, in **batches of 5,000 rows**.

The data is loaded into the `sales` table.

The pipeline uses PostgreSQL `ON CONFLICT` logic on `order_id` to update an existing order instead of creating a duplicate record, making reruns idempotent.

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

## Synthetic Test Data

`generate_data.py` generates a configurable volume of realistic synthetic sales records using Faker, with intentionally injected data quality issues (negative quantities, missing prices, duplicate order IDs) so the validation logic is exercised against realistic conditions rather than clean toy data.

```bash
python generate_data.py
```

## Testing

Unit tests cover the transformation and validation logic using `pytest`:

```bash
pytest tests/ -v
```

Current coverage includes: total amount calculation, quarantining of invalid quantity/price/duplicate rows, date conversion, and the all-rows-invalid failure case.

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

### 6. (Optional) Generate synthetic data

```powershell
python generate_data.py
```

### 7. Run the pipeline

From the project root:

```powershell
cd src
python main.py
```

### 8. Run tests

From the project root:

```powershell
pytest tests/ -v
```

## Sample Pipeline Output

```text
ETL pipeline started
Extracted 50000 rows from CSV
Dropping 1036 rows with invalid quantity (<= 0)
Dropping 506 rows with invalid/missing price
Dropping 768 duplicate order_id rows (keeping first occurrence)
Quarantined 2267 of 50000 rows (47733 rows passed validation)
Loaded batch 1: 5000 rows
...
Loaded 47733 rows into PostgreSQL
ETL pipeline completed successfully
```

The loaded records were verified in PostgreSQL using pgAdmin.

## Error Handling and Logging

The pipeline includes:

* Exception handling during extraction, transformation, and loading.
* Informative logging for pipeline execution.
* Row-level data quality quarantining with an auditable output file.
* Database transaction handling.
* PostgreSQL conflict handling for duplicate order IDs, enabling idempotent reruns.

## Future Enhancements

Planned improvements for future phases include:

* Automated pipeline scheduling with Apache Airflow.
* Docker containerization.
* Cloud data warehouse integration (Snowflake).
* Incremental/streaming data processing.
* Integration tests against a test database.
* CI pipeline (GitHub Actions) running tests on every push.

## Project Status

**Phase 1 - Completed and hardened**

Current implementation:

**CSV -> Python/Pandas ETL (quarantine-based validation) -> PostgreSQL (batched, idempotent upserts) -> pytest test suite**

Future phases will focus on orchestration, containerization, scalability, and cloud integration.