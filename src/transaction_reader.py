import csv
import os
from typing import Any, Dict, List

import pandas as pd


def load_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает CSV файл по переданному полному пути.
    Возвращает список словарей.
    """
    if not os.path.isfile(file_path):
        print(f" Файл не найден (CSV): {file_path}")
        return []

    try:
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            transactions = list(reader)
            print(f" CSV успешно загружен: {len(transactions)} транзакций")
            return transactions
    except Exception as e:
        print(f" Ошибка при чтении CSV: {e}")
        return []


def load_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Excel файл по переданному полному пути.
    Возвращает список словарей.
    """

    if not os.path.isfile(file_path):
        print(f"Файл не найден (Excel): {file_path}")
        return []

    try:
        df = pd.read_excel(file_path)
        transactions = df.to_dict(orient="records")
        print(f"Excel успешно загружен: {len(transactions)} записей")
        return transactions
    except Exception as e:
        print(f"Ошибка при чтении Excel: {e}")
        return []
