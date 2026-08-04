# tests/test_search_operation.py
import pytest
from unittest.mock import patch, mock_open
import pandas as pd
from src.transaction_reader import load_csv_transactions, load_excel_transactions


def test_csv_returns_list_of_dicts() -> None:
    csv_content = "id,amount,currency\n1,100,USD\n2,200,EUR"
    m = mock_open(read_data=csv_content)

    with patch("src.transaction_reader.open", m):
        # Важно: подменяем os.path.isfile, чтобы тест не зависел от реальных файлов
        with patch("src.transaction_reader.os.path.isfile", return_value=True):
            result = load_csv_transactions("dummy.csv")

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["id"] == "1"


def test_csv_file_not_found_returns_empty_list() -> None:
    with patch("src.transaction_reader.os.path.isfile", return_value=False):
        result = load_csv_transactions("missing.csv")
    assert result == []


def test_excel_returns_list_of_dicts() -> None:
    mock_df = pd.DataFrame([
        {"id": 1, "amount": 100.0, "currency": "USD"},
        {"id": 2, "amount": 200.0, "currency": "EUR"},
    ])

    with patch("src.transaction_reader.pd.read_excel", return_value=mock_df):
        with patch("src.transaction_reader.os.path.isfile", return_value=True):
            result = load_excel_transactions("dummy.xlsx")

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["currency"] == "USD"


def test_excel_handles_read_error_gracefully() -> None:
    with patch("src.transaction_reader.os.path.isfile", return_value=True):
        with patch("src.transaction_reader.pd.read_excel", side_effect=Exception("read error")):
            result = load_excel_transactions("broken.xlsx")
    assert result == []