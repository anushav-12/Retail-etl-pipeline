import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pandas as pd
import pytest
from transform import transform_data


def make_df(rows):
    return pd.DataFrame(rows)


def test_total_amount_calculated_correctly():
    df = make_df([
        {"order_id": 1, "order_date": "2024-01-01", "quantity": 3, "price": 100}
    ])
    result = transform_data(df)
    assert result.loc[0, "total_amount"] == 300


def test_negative_quantity_is_quarantined_not_loaded():
    df = make_df([
        {"order_id": 1, "order_date": "2024-01-01", "quantity": -2, "price": 100},
        {"order_id": 2, "order_date": "2024-01-01", "quantity": 1, "price": 100},
    ])
    result = transform_data(df)
    assert len(result) == 1
    assert result.iloc[0]["order_id"] == 2


def test_missing_price_is_quarantined():
    df = make_df([
        {"order_id": 1, "order_date": "2024-01-01", "quantity": 1, "price": None},
        {"order_id": 2, "order_date": "2024-01-01", "quantity": 1, "price": 50},
    ])
    result = transform_data(df)
    assert len(result) == 1
    assert result.iloc[0]["order_id"] == 2


def test_duplicate_order_id_keeps_first_occurrence():
    df = make_df([
        {"order_id": 1, "order_date": "2024-01-01", "quantity": 1, "price": 50},
        {"order_id": 1, "order_date": "2024-01-02", "quantity": 2, "price": 60},
    ])
    result = transform_data(df)
    assert len(result) == 1
    assert result.iloc[0]["price"] == 50  # first occurrence kept


def test_order_date_converted_to_datetime():
    df = make_df([
        {"order_id": 1, "order_date": "2024-01-15", "quantity": 1, "price": 10}
    ])
    result = transform_data(df)
    assert pd.api.types.is_datetime64_any_dtype(result["order_date"])


def test_all_rows_invalid_raises_error():
    df = make_df([
        {"order_id": 1, "order_date": "2024-01-01", "quantity": -1, "price": 100}
    ])
    with pytest.raises(ValueError):
        transform_data(df)


def test_valid_rows_pass_through_untouched():
    df = make_df([
        {"order_id": 1, "order_date": "2024-01-01", "quantity": 2, "price": 50},
        {"order_id": 2, "order_date": "2024-01-02", "quantity": 3, "price": 30},
    ])
    result = transform_data(df)
    assert len(result) == 2