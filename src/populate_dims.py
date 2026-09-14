from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

password = os.getenv("DB_PASSWORD")
engine = create_engine(
    f"postgresql+psycopg2://postgres:{password}@localhost:5432/retail_pipeline"
)

with engine.begin() as connection:
    # ---- dim_customer ----
    customers = connection.execute(text("""
        SELECT DISTINCT customer_id
        FROM sales
        WHERE customer_id IS NOT NULL
    """)).fetchall()

    customer_rows = [{"customer_id": row[0]} for row in customers]

    connection.execute(text("""
        INSERT INTO dim_customer (customer_id)
        VALUES (:customer_id)
        ON CONFLICT (customer_id) DO NOTHING
    """), customer_rows)

    print(f"Inserted {len(customer_rows)} rows into dim_customer")

    # ---- dim_product ----
    products = connection.execute(text("""
        SELECT DISTINCT product, category
        FROM sales
        WHERE product IS NOT NULL
    """)).fetchall()

    product_rows = [
        {"product_id": row[0], "product_name": row[0], "category": row[1]}
        for row in products
    ]

    connection.execute(text("""
        INSERT INTO dim_product (product_id, product_name, category)
        VALUES (:product_id, :product_name, :category)
        ON CONFLICT (product_id) DO NOTHING
    """), product_rows)

    print(f"Inserted {len(product_rows)} rows into dim_product")