from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import date, timedelta
import os

load_dotenv()

password = os.getenv("DB_PASSWORD")
engine = create_engine(
    f"postgresql+psycopg2://postgres:{password}@localhost:5432/retail_pipeline"
)

start_date = date(2020, 1, 1)
end_date = date(2026, 12, 31)

current = start_date
rows = []
while current <= end_date:
    date_key = int(current.strftime("%Y%m%d"))
    rows.append({
        "date_key": date_key,
        "full_date": current,
        "day": current.day,
        "month": current.month,
        "month_name": current.strftime("%B"),
        "quarter": (current.month - 1) // 3 + 1,
        "year": current.year,
        "day_of_week": current.strftime("%A"),
        "is_weekend": current.weekday() >= 5
    })
    current += timedelta(days=1)

insert_query = text("""
    INSERT INTO dim_date (date_key, full_date, day, month, month_name, quarter, year, day_of_week, is_weekend)
    VALUES (:date_key, :full_date, :day, :month, :month_name, :quarter, :year, :day_of_week, :is_weekend)
    ON CONFLICT (date_key) DO NOTHING
""")

with engine.begin() as connection:
    connection.execute(insert_query, rows)

print(f"Inserted {len(rows)} rows into dim_date")