import pytest
from unittest.mock import patch, mock_open
import pandas as pd
from src.transaction_reader import load_csv_transactions, load_excel_transactions


class TestCSVReader:
    @patch("src.transaction_reader.os.path.isfile", return_value=True)
    def test_csv_returns_list_of_dicts(self, mock_isfile):
        csv_content = "id,amount,state\n1,100,EXECUTED\n2,200,PENDING"
        m = mock_open(read_data=csv_content)

        with patch("src.transaction_reader.open", m):
            result = load_csv_transactions("dummy.csv")

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == "1"
        assert result[1]["state"] == "PENDING"

    @patch("src.transaction_reader.os.path.isfile", return_value=False)
    def test_csv_file_not_found(self, mock_isfile):
        result = load_csv_transactions("missing.csv")
        assert result == []


class TestExcelReader:
    @patch("src.transaction_reader.os.path.isfile", return_value=True)
    @patch("src.transaction_reader.pd.read_excel")
    def test_excel_returns_list_of_dicts(self, mock_read_excel, mock_isfile):
        mock_df = pd.DataFrame([
            {"id": 1, "amount": 100.0, "state": "EXECUTED"},
            {"id": 2, "amount": 200.0, "state": "PENDING"},
        ])
        mock_read_excel.return_value = mock_df

        result = load_excel_transactions("dummy.xlsx")

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["state"] == "EXECUTED"

    @patch("src.transaction_reader.os.path.isfile", return_value=False)
    def test_excel_file_not_found(self, mock_isfile):
        result = load_excel_transactions("missing.xlsx")
        assert result == []