import logging

from extract import extract_data
from transform import transform_data
from load import load_data


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():

    logging.info("ETL pipeline started")

    try:
        # Extract
        data = extract_data()

        # Transform
        transformed_data = transform_data(data)

        # Load
        load_data(transformed_data)

        logging.info("ETL pipeline completed successfully")

    except Exception as e:
        logging.error(f"ETL pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main()