import pandas as pd
import logging


def transform_data(data):

    try:
        # Calculate total amount
        data["total_amount"] = data["quantity"] * data["price"]

        # Check for missing values
        null_counts = data.isnull().sum()

        if null_counts.any():
            logging.warning(f"Missing values found:\n{null_counts}")

        # Convert order_date to datetime
        data["order_date"] = pd.to_datetime(data["order_date"])

        # Validate quantity
        if (data["quantity"] <= 0).any():
            raise ValueError("Quantity must be greater than 0")

        # Validate price
        if (data["price"] <= 0).any():
            raise ValueError("Price must be greater than 0")

        # Check duplicate order IDs
        if data["order_id"].duplicated().any():
            raise ValueError("Duplicate order_id found")

        logging.info("Transformation and validation completed successfully")

        return data

    except Exception as e:
        logging.error(f"Transformation failed: {e}")
        raise