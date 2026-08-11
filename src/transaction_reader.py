# src/transaction_reader.py
import csv
import json
import os
from typing import Any, Dict, List

try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

RowType = Dict[Any, Any]


def load_csv_transactions(file_path: str) -> list[dict[str, Any]]:
    """Загрузка Csv файла"""
    if not os.path.isfile(file_path):
        print(f" Файл не найден (CSV): {file_path}")
        return []
    try:
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            transactions = [row for row in reader if any(row.values())]
            print(f" CSV успешно загружен: {len(transactions)} транзакций")
            return transactions
    except Exception as e:
        print(f" Ошибка при чтении CSV: {e}")
        return []


def load_excel_transactions(file_path: str) -> List[RowType]:
    """Загрузка Excel файла"""
    if not PANDAS_AVAILABLE:
        print(" pandas не установлен, чтение Excel недоступно")
        return []
    if not os.path.isfile(file_path):
        print(f" Файл не найден (Excel): {file_path}")
        return []
    try:
        df = pd.read_excel(file_path)
        # Очищаем строки от NaN значений, превращая их в None
        df = df.where(pd.notnull(df), None)
        transactions = df.to_dict(orient="records")
        print(f" Excel успешно загружен: {len(transactions)} записей")
        return transactions
    except Exception as e:
        print(f" Ошибка чтения Excel: {e}")
        return []


def load_json_transactions(file_path: str) -> List[RowType]:
    """Загрузка json файла"""
    if not os.path.isfile(file_path):
        print(f" Файл не найден (JSON): {file_path}")
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            raw_transactions = data
        elif isinstance(data, dict) and "transactions" in data:
            raw_transactions = data["transactions"]
        else:
            print(" Неожиданная структура JSON")
            return []

        cleaned: List[RowType] = []
        for row in raw_transactions:
            if not isinstance(row, dict):
                continue
            cleaned.append({str(k): v for k, v in row.items()})

        print(f" JSON успешно загружен: {len(cleaned)} транзакций")
        return cleaned
    except Exception as e:
        print(f" Ошибка чтения JSON: {e}")
        return []
