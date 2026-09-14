from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

password = os.getenv("DB_PASSWORD")
engine = create_engine(
    f"postgresql+psycopg2://postgres:{password}@localhost:5432/retail_pipeline"
)

with engine.begin() as connection:
    result = connection.execute(text("""
        INSERT INTO fact_orders (
            order_id, customer_key, product_key, date_key,
            quantity, unit_price, total_amount, order_status
        )
        SELECT
            s.order_id,
            c.customer_key,
            p.product_key,
            CAST(TO_CHAR(s.order_date, 'YYYYMMDD') AS INT) AS date_key,
            s.quantity,
            s.price,
            s.total_amount,
            'completed' AS order_status
        FROM sales s
        JOIN dim_customer c ON s.customer_id = c.customer_id
        JOIN dim_product p ON s.product = p.product_id
        WHERE s.order_id IS NOT NULL
        ON CONFLICT (order_id) DO NOTHING
    """))

    print(f"Inserted {result.rowcount} rows into fact_orders")