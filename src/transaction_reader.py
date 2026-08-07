import csv
import json
import os
import typing as t

try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("ВНИМАНИЕ: pandas не установлен. Чтение Excel будет недоступно.")

RowType = t.Dict[t.Any, t.Any]


def load_csv_transactions(file_path: str) -> list[RowType]:
    """
    Читает CSV файл по переданному полному пути.
    Возвращает список словарей. При ошибке — пустой список.
    """
    if not os.path.isfile(file_path):
        print(f"Файл не найден (CSV): {file_path}")
        return []

    try:
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            transactions = list(reader)
            print(f"CSV успешно загружен: {len(transactions)} транзакций")
            return transactions
    except Exception as e:
        print(f"Ошибка при чтении CSV: {e}")
        return []


def load_excel_transactions(file_path: str) -> list[RowType]:
    """
    Читает Excel файл по переданному полному пути.
    Возвращает список словарей. При ошибке или отсутствии pandas — пустой список.
    """
    if not PANDAS_AVAILABLE:
        print("pandas не установлен, чтение Excel невозможно.")
        return []

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


def load_json_transactions(file_path: str) -> list[RowType]:
    """
    Заглушка для чтения JSON: читает файл и возвращает список словарей.
    При ошибке или отсутствии файла — пустой список.
    Реализована для возможности вызова из main.
    """
    if not os.path.isfile(file_path):
        print(f"Файл не найден (JSON): {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            print(f"JSON успешно загружен: {len(data)} записей")
            return data

        if isinstance(data, dict):
            result = [data]
            print("JSON успешно загружен: 1 запись (преобразована в список)")
            return result

        print("Неподдерживаемая структура JSON: ожидается список или словарь.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении JSON: {e}")
        return []


if __name__ == "__main__":
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    project_root = os.path.dirname(current_dir)
    data_dir = os.path.join(project_root, "data")

    print(f"Корень проекта: {project_root}")
    print(f"Папка data: {data_dir}")

    csv_full_path = os.path.join(data_dir, "transactions.csv")
    excel_full_path = os.path.join(data_dir, "transactions_excel.xlsx")
    json_full_path = os.path.join(data_dir, "transactions.json")

    print(f"\nПопытка чтения: {csv_full_path}")
    csv_data = load_csv_transactions(csv_full_path)

    for i, row in enumerate(csv_data[:5]):
        print(f"{i + 1}. {row}")

    print(f"\nПопытка чтения: {excel_full_path}")
    excel_data = load_excel_transactions(excel_full_path)

    for i, row in enumerate(excel_data[:5]):
        print(f"{i + 1}. {row}")

    print(f"\nПопытка чтения: {json_full_path}")
    json_data = load_json_transactions(json_full_path)

    for i, row in enumerate(json_data[:5]):
        print(f"{i + 1}. {row}")

    print("\nГотово")
