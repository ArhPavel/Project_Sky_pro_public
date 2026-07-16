from typing import Any

from src.Utils import load_transactions


def test_load_valid_json(tmp_path: Any) -> None:
    # Создаём data/operations.json относительно tmp_path для теста
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    operations_file = data_dir / "operations.json"

    operations_file.write_text("""[
          {"id": 1, "amount": 1500.50, "currency": "RUB", "type": "income", "date": "2024-06-01"},
          {"id": 2, "amount": -800.00, "currency": "RUB", "type": "expense", "date": "2024-06-03"}
        ]""")

    transactions = load_transactions(str(operations_file))
    assert isinstance(transactions, list)
    assert len(transactions) == 2
    assert transactions[0]["type"] == "income"
    assert transactions[1]["amount"] == -800.0


def test_load_nonexistent_file() -> None:
    transactions = load_transactions("this_file_does_not_exist.json")
    assert transactions == []


def test_load_empty_file(tmp_path: Any) -> None:
    empty_file = tmp_path / "empty.json"
    empty_file.write_text("")
    transactions = load_transactions(str(empty_file))
    assert transactions == []


def test_load_not_a_list_json(tmp_path: Any) -> None:
    bad_file = tmp_path / "bad.json"
    bad_file.write_text('{"not": "a list"}')
    transactions = load_transactions(str(bad_file))
    assert transactions == []


def test_load_invalid_json(tmp_path: Any) -> None:
    bad_file = tmp_path / "invalid.json"
    bad_file.write_text("{not valid json}")
    transactions = load_transactions(str(bad_file))
    assert transactions == []
