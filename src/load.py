from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import logging
import os

load_dotenv()

def load_data(df):
    try:
        password = os.getenv("DB_PASSWORD")

        engine = create_engine(
            f"postgresql+psycopg2://postgres:{password}@localhost:5432/retail_pipeline"
        )

        records = df.to_dict(orient="records")

        insert_query = text("""
            INSERT INTO sales (
                order_id, order_date, customer_id, product,
                category, quantity, price, total_amount
            )
            VALUES (
                :order_id, :order_date, :customer_id, :product,
                :category, :quantity, :price, :total_amount
            )
            ON CONFLICT (order_id)
            DO UPDATE SET
                order_date = EXCLUDED.order_date,
                customer_id = EXCLUDED.customer_id,
                product = EXCLUDED.product,
                category = EXCLUDED.category,
                quantity = EXCLUDED.quantity,
                price = EXCLUDED.price,
                total_amount = EXCLUDED.total_amount
        """)

        batch_size = 5000
        with engine.begin() as connection:
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                connection.execute(insert_query, batch)
                logging.info(f"Loaded batch {i // batch_size + 1}: {len(batch)} rows")

        logging.info(f"Loaded {len(df)} rows into PostgreSQL")

    except Exception as e:
        logging.error(f"Database load failed: {e}")
        raise