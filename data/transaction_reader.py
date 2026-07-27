import csv
import os

import pandas as pd

"""Функция чтения из файла .xlsx и .csv"""

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# НАСТРОЙКА ПУТЕЙ (работает из папки data/)

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)
project_root = os.path.dirname(current_dir)  # Поднимаемся из data/ в корень проекта

print(f"=== Корень проекта: {project_root} ===")

# ФУНКЦИЯ ДЛЯ CSV (возвращает список словарей)
# ==========================================


def load_csv_transactions(filename: str) -> list:
    file_path = os.path.join(project_root, filename)

    if not os.path.isfile(file_path):
        print(f" Файл не найден: {file_path}")
        return []

    try:
        with open(file_path, newline="", encoding="utf-8") as f:
            # DictReader создает словари на основе заголовков первой строки
            reader = csv.DictReader(f)
            transactions = list(reader)
            print(f"CSV успешно загружен: {len(transactions)} транзакций")
            return transactions
    except Exception as e:
        print(f"Ошибка при чтении CSV: {e}")
        return []


# ==========================================
#  ФУНКЦИЯ ДЛЯ EXCEL (возвращает список словарей)
# ==========================================
def load_excel_transactions(filename: str) -> list:
    file_path = os.path.join(project_root, filename)

    if not os.path.isfile(file_path):
        print(f" Файл Excel не найден: {file_path}")
        return []

    try:
        df = pd.read_excel(file_path)
        # Конвертируем DataFrame в список словарей (формат как у CSV)
        transactions = df.to_dict(orient="records")
        print(f"Excel успешно загружен: {len(transactions)} записей")
        return transactions
    except Exception as e:
        print(f"Ошибка при чтении Excel: {e}")
        return []

# ОСНОВНОЙ БЛОК ВЫПОЛНЕНИЯ

# Чтение CSV


csv_filename = "transactions.csv"

csv_path = os.path.join(project_root, csv_filename)
print(f"\n Путь к CSV: {csv_path}")


print(f" Существует? {os.path.isfile(csv_path)}")

csv_data = load_csv_transactions(csv_filename)

print("\n--- Первые 5 транзакций из CSV (список словарей) ---")
for i, row in enumerate(csv_data[:5]):
    print(f"{i + 1}. {row}")

# Чтение Excel


excel_filename = "transactions_excel.xlsx"

excel_path = os.path.join(project_root, excel_filename)
print(f"\n Путь к Excel: {excel_path}")
print(f" Существует? {os.path.isfile(excel_path)}")

excel_data = load_excel_transactions(excel_filename)

print("\n--- Первые 5 записей из Excel (список словарей) ---")
for i, row in enumerate(excel_data[:5]):
    print(f"{i + 1}. {row}")

print("\n=== Готово ===")
