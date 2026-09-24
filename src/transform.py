import pandas as pd
import logging
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUARANTINE_DIR = os.path.join(BASE_DIR, "..", "data", "processed")
QUARANTINE_PATH = os.path.join(QUARANTINE_DIR, "quarantined_rows.csv")


def transform_data(data):
    try:
        original_count = len(data)

        data["total_amount"] = data["quantity"] * data["price"]

        null_counts = data.isnull().sum()
        if null_counts.any():
            logging.warning(f"Missing values found:\n{null_counts}")

        data["order_date"] = pd.to_datetime(data["order_date"])

        invalid_mask = pd.Series(False, index=data.index)

        # --- existing checks ---
        bad_quantity = data["quantity"] <= 0
        if bad_quantity.any():
            logging.warning(f"Dropping {bad_quantity.sum()} rows with invalid quantity (<= 0)")
            invalid_mask |= bad_quantity

        bad_price = data["price"].isnull() | (data["price"] <= 0)
        if bad_price.any():
            logging.warning(f"Dropping {bad_price.sum()} rows with invalid/missing price")
            invalid_mask |= bad_price

        dup_order_id = data["order_id"].duplicated(keep="first")
        if dup_order_id.any():
            logging.warning(f"Dropping {dup_order_id.sum()} duplicate order_id rows (keeping first occurrence)")
            invalid_mask |= dup_order_id

        # --- new checks ---
        null_order_id = data["order_id"].isnull()
        if null_order_id.any():
            logging.warning(f"Dropping {null_order_id.sum()} rows with null order_id")
            invalid_mask |= null_order_id

        null_customer = data["customer_id"].isnull()
        if null_customer.any():
            logging.warning(f"Dropping {null_customer.sum()} rows with null customer_id")
            invalid_mask |= null_customer

        null_product = data["product"].isnull()
        if null_product.any():
            logging.warning(f"Dropping {null_product.sum()} rows with null product")
            invalid_mask |= null_product

        today = pd.Timestamp(datetime.now().date())
        min_valid_date = pd.Timestamp("2015-01-01")
        bad_date = data["order_date"].isnull() | (data["order_date"] > today) | (data["order_date"] < min_valid_date)
        if bad_date.any():
            logging.warning(f"Dropping {bad_date.sum()} rows with invalid/out-of-range order_date")
            invalid_mask |= bad_date

        # --- quarantine + return ---
        quarantined = data[invalid_mask]
        clean_data = data[~invalid_mask].copy()

        if not quarantined.empty:
            os.makedirs(QUARANTINE_DIR, exist_ok=True)
            quarantined.to_csv(QUARANTINE_PATH, index=False)
            logging.warning(
                f"Quarantined {len(quarantined)} of {original_count} rows "
                f"({len(clean_data)} rows passed validation)"
            )

        if clean_data.empty:
            raise ValueError("No valid rows remaining after validation — aborting load")

        logging.info(
            f"Transformation and validation completed: "
            f"{len(clean_data)}/{original_count} rows valid"
        )
        return clean_data

    except Exception as e:
        logging.error(f"Transformation failed: {e}")
        raise
