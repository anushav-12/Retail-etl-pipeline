import pandas as pd


def extract_data():
    file_path = "../data/raw/sales_data.csv"

    df = pd.read_csv(file_path)

    return df


if __name__ == "__main__":
    data = extract_data()

    print(data)
    print("\nTotal rows:", len(data))