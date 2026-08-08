import csv
import json
import os
from typing import Any, Dict, List, Optional, Tuple

try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

# Используем Any для ключей, чтобы mypy не ругался на csv.DictReader
RowType = Dict[Any, Any]


def _log(message: str) -> None:
    """Заглушка для логгера. Позже можно заменить на logger.info(...)"""
    print(message)


def load_csv_transactions(
    file_path: str,
    delimiter: str = ";",
    encoding: str = "utf-8"
) -> List[RowType]:
    if not os.path.isfile(file_path):
        _log(f" Файл не найден (CSV): {file_path}")
        return []

    try:
        with open(file_path, newline="", encoding=encoding) as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            transactions = list(reader)
            _log(f" CSV: {len(transactions)} транзакций (delimiter={delimiter!r})")
            return transactions
    except Exception as e:
        _log(f" Ошибка чтения CSV: {e}")
        return []


def load_excel_transactions(file_path: str) -> List[RowType]:
    if not PANDAS_AVAILABLE:
        _log(" pandas не установлен, чтение Excel недоступно")
        return []

    if not os.path.isfile(file_path):
        _log(f" Файл не найден (Excel): {file_path}")
        return []

    try:
        df = pd.read_excel(file_path)
        transactions = df.to_dict(orient="records")
        _log(f" Excel: {len(transactions)} записей")
        return transactions
    except Exception as e:
        _log(f" Ошибка чтения Excel: {e}")
        return []


def load_json_transactions(file_path: str) -> List[RowType]:
    if not os.path.isfile(file_path):
        _log(f" Файл не найден (JSON): {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            raw_transactions = data
        elif isinstance(data, dict) and "transactions" in data:
            raw_transactions = data["transactions"]
        else:
            _log(" Неожиданная структура JSON: ожидается список или объект с ключом 'transactions'")
            return []

        # Приводим ключи к str и фильтруем только dict-строки
        cleaned: List[RowType] = []
        for row in raw_transactions:
            if not isinstance(row, dict):
                continue
            cleaned.append({str(k): v for k, v in row.items()})

        _log(f" JSON: {len(cleaned)} транзакций")
        return cleaned
    except Exception as e:
        _log(f" Ошибка чтения JSON: {e}")
        return []


def sort_by_amount(
    transactions: List[RowType],
    field: str = "amount"
) -> List[RowType]:
    """Сортировка по числовому полю (например, amount). Невалидные значения считаются как 0.0."""

    def sort_key_safe(row: RowType) -> float:
        value = row.get(field)
        if value is None:
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    return sorted(transactions, key=sort_key_safe)


def sort_by_status(
    transactions: List[RowType],
    status_order: Optional[List[str]] = None
) -> List[RowType]:
    """
    Сортирует транзакции по статусу.
    Приоритет по умолчанию: EXECUTED, CANCELED, PENDING.
    Транзакции с неизвестным статусом идут в конец.
    Если у транзакции нет id — он заменяется на пустую строку для безопасного сравнения.
    """
    if status_order is None:
        status_order = ["EXECUTED", "CANCELED", "PENDING"]

    # Создаём словарь приоритетов для быстрого поиска
    priority = {status: idx for idx, status in enumerate(status_order)}
    max_prio = len(status_order)

    def sort_key(row: RowType) -> Tuple[int, str]:
        # Проверяем оба варианта ключа: 'state' и 'status'
        status = row.get("state") or row.get("status") or ""
        prio = priority.get(status, max_prio)

        tx_id = row.get("id")
        id_str = str(tx_id) if tx_id is not None else ""

        return (prio, id_str)

    return sorted(transactions, key=sort_key)


if __name__ == "__main__":
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)  # src/
    project_root = os.path.dirname(current_dir)  # корень проекта
    data_dir = os.path.join(project_root, "data")

    _log(f"=== Корень проекта: {project_root} ===")
    _log(f"=== Папка data: {data_dir} ===")

    csv_path = os.path.join(data_dir, "transactions.csv")
    excel_path = os.path.join(data_dir, "transactions_excel.xlsx")
    json_path = os.path.join(data_dir, "transactions.json")

    all_transactions: List[RowType] = []

    # Загрузка
    all_transactions.extend(load_csv_transactions(csv_path))
    all_transactions.extend(load_excel_transactions(excel_path))
    all_transactions.extend(load_json_transactions(json_path))

    _log(f"\n📊 Всего загружено транзакций: {len(all_transactions)}")

    # Сортировка по статусу
    sorted_transactions = sort_by_status(all_transactions)

    _log("\n--- Первые 10 транзакций (отсортировано по статусу) ---")
    for i, row in enumerate(sorted_transactions[:10]):
        status = row.get("status", row.get("state", "NO_STATUS"))
        tx_id = row.get("id", "NO_ID")
        # Для отладки можно выводить только ключевые поля, а не весь row
        print(f"{i + 1}. ID={tx_id}, status={status}, row={row}")

    _log("\n=== Готово ===")
