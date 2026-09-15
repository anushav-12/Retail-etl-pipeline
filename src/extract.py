import pandas as pd
import logging
import os


def extract_data():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "data", "raw", "sales_data.csv")

    try:
        df = pd.read_csv(file_path)

        logging.info(f"Extracted {len(df)} rows from CSV")

        return df

    except Exception as e:
        logging.error(f"Failed to extract data: {e}")
        raise


if __name__ == "__main__":
    data = extract_data()

    print(data)
    print("\nTotal rows:", len(data))