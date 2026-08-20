from faker import Faker
import random
import pandas as pd

fake = Faker()
random.seed(42)

categories = {
    "Electronics": ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones"],
    "Grocery": ["Rice 5kg", "Milk 1L", "Eggs Dozen", "Bread"],
    "Apparel": ["T-Shirt", "Jeans", "Jacket", "Sneakers"],
}

rows = []
for order_id in range(1000, 51000):  # 50k orders
    category = random.choice(list(categories.keys()))
    product = random.choice(categories[category])
    quantity = random.randint(1, 5)
    price = round(random.uniform(50, 80000), 2)

    # inject realistic messiness on purpose
    if random.random() < 0.02:
        quantity = -1              # bad data: negative qty
    if random.random() < 0.01:
        price = None               # missing value
    if random.random() < 0.015 and rows:
        order_id = rows[-1]["order_id"]  # duplicate order_id

    rows.append({
        "order_id": order_id,
        "order_date": fake.date_between(start_date="-180d", end_date="today"),
        "customer_id": random.randint(1, 5000),
        "product": product,
        "category": category,
        "quantity": quantity,
        "price": price,
    })

df = pd.DataFrame(rows)
import os

output_path = os.path.abspath("data/raw/sales_data.csv")
print("Writing to:", output_path)
print("Current working directory:", os.getcwd())

df.to_csv(output_path, index=False)

print(f"Generated {len(df)} rows")
print("File size after write:", os.path.getsize(output_path), "bytes")
print("File modified time:", os.path.getmtime(output_path))