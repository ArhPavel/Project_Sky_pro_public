# main.py
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.masks import get_mask_account, mask_card_full
from src.processing import (count_by_category, filter_by_state, filter_rub_transactions, process_bank_search,
                            sort_by_date)
from src.transaction_reader import load_csv_transactions, load_excel_transactions, load_json_transactions

project_root = os.getcwd()
data_dir = os.path.join(project_root, "data")

csv_path = os.path.join(data_dir, "transactions.csv")
excel_path = os.path.join(data_dir, "transactions_excel.xlsx")
json_path = os.path.join(data_dir, "transactions.json")


def get_valid_status() -> str:
    allowed = {"EXECUTED", "CANCELED", "PENDING"}
    while True:
        user_input = input(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING\n> "
        ).strip()
        status = user_input.upper()
        if status in allowed:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status
        else:
            print(f'Статус операции "{user_input}" недоступен.')


def format_currency_amount(amount: Any, currency: Optional[str]) -> str:
    try:
        val = float(amount)
    except (ValueError, TypeError):
        return str(amount or "0")

    currency_upper = (currency or "").upper()
    if currency_upper == "RUB":
        return f"{val:,.0f} руб.".replace(",", " ")
    elif currency_upper in ("USD", "EUR"):
        return f"{val:,.2f} {currency_upper}".replace(",", " ")
    else:
        return f"{val:,.2f} {currency_upper or '???'}"


def mask_sensitive_info(transaction: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(transaction, dict):
        return {}

    tx = {str(k): v for k, v in transaction.items()}

    # Проверяем как прямые ключи, так и вложенные структуры (например, из JSON)
    card_from = tx.get("card_number_from") or tx.get("from")
    card_to = tx.get("card_number_to") or tx.get("to")
    account_from = tx.get("account_from")
    account_to = tx.get("account_to")

    # Умное разделение счетов и карт, если они записаны в одно поле 'from' / 'to'
    if card_from and "счет" in str(card_from).lower():
        account_from = "".join(filter(str.isdigit, str(card_from)))
        card_from = None
    elif card_from:
        card_from = "".join(filter(str.isdigit, str(card_from)))

    if card_to and "счет" in str(card_to).lower():
        account_to = "".join(filter(str.isdigit, str(card_to)))
        card_to = None
    elif card_to:
        card_to = "".join(filter(str.isdigit, str(card_to)))

    tx["_masked_card_from"] = mask_card_full(str(card_from)) if card_from and len(str(card_from)) == 16 else None
    tx["_masked_card_to"] = mask_card_full(str(card_to)) if card_to and len(str(card_to)) == 16 else None
    tx["_masked_account_from"] = get_mask_account(str(account_from)) if account_from else None
    tx["_masked_account_to"] = get_mask_account(str(account_to)) if account_to else None

    return tx


def parse_date_to_datetime(date_raw: Any) -> Optional[datetime]:
    if isinstance(date_raw, datetime):
        return date_raw
    if not isinstance(date_raw, str):
        return None

    date_str = date_raw.strip()
    if not date_str:
        return None

    if date_str.endswith("Z"):
        date_str = date_str[:-1]

    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def print_transaction(tx: Dict[str, Any], idx: int) -> None:
    date_raw = tx.get("date")
    description = tx.get("description") or tx.get("operation") or "Неизвестная операция"

    # Извлечение суммы и валюты из плоской или вложенной структуры данных
    amount = tx.get("amount") or tx.get("operationAmount", {}).get("amount")
    currency = (
        tx.get("currency") or tx.get("operationAmount", {}).get("currency", {}).get("code") or tx.get("currency_code")
    )

    dt = parse_date_to_datetime(date_raw)
    date_str = dt.strftime("%d.%m.%Y") if dt else str(date_raw or "??.??.????")

    print(f"{idx}. {date_str} — {description}")

    card_from = tx.get("_masked_card_from")
    card_to = tx.get("_masked_card_to")
    account_from = tx.get("_masked_account_from")
    account_to = tx.get("_masked_account_to")

    line_middle = ""
    if card_from and card_to:
        line_middle = f"  {card_from} → {card_to}"
    elif card_from and account_to:
        line_middle = f"  {card_from} → счёт {account_to}"
    elif account_from and card_to:
        line_middle = f"  счёт {account_from} → {card_to}"
    elif account_from and account_to:
        line_middle = f"  счёт {account_from} → счёт {account_to}"
    elif card_from:
        line_middle = f"  {card_from}"
    elif account_from:
        line_middle = f"  счёт {account_from}"
    elif card_to:
        line_middle = f"  {card_to}"
    elif account_to:
        line_middle = f"  счёт {account_to}"

    if line_middle:
        print(line_middle)

    print(f"  Сумма: {format_currency_amount(amount, currency)}\n")


def print_category_stats(transactions: List[Dict[str, Any]]) -> None:
    counter = count_by_category(transactions)
    if not counter:
        print("Статистика по категориям недоступна (нет транзакций).")
        return

    total = sum(counter.values())
    print("--- Статистика по категориям ---")
    for category, count in counter.most_common():
        percent = (count / total) * 100
        print(f"  {category.capitalize()}: {count} шт. ({percent:.1f}%)")
    print()


def main() -> None:
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ").strip()
    all_transactions: List[Dict[str, Any]] = []

    if choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        all_transactions = load_json_transactions(json_path)
    elif choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        all_transactions = load_csv_transactions(csv_path)
    elif choice == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
        all_transactions = load_excel_transactions(excel_path)
    else:
        print("Программа: Неверный выбор. Завершение работы.")
        return

    if not all_transactions:
        print("Программа: Не найдено ни одной транзакции в выбранном файле.")
        return

    target_status = get_valid_status()
    working_list = filter_by_state(all_transactions, state=target_status)

    if not working_list:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    sort_date_input = input("Программа: Отсортировать операции по дате? Да/Нет\n> ").strip().lower()
    sorted_result = working_list

    if sort_date_input in ("да", "д", "yes", "y"):
        order_input = input("Программа: По возрастанию или по убыванию?\n> ").strip().lower()
        reverse_order = order_input in ("убыванию", "по убыванию", "desc", "down")
        sorted_result = sort_by_date(working_list, reverse_order=reverse_order)

    rub_only_input = input("Программа: Выводить только рублёвые транзакции? Да/Нет\n> ").strip().lower()
    if rub_only_input in ("да", "д", "yes", "y"):
        sorted_result = filter_rub_transactions(sorted_result)
        print("Отфильтрованы только RUB транзакции.")
    else:
        print("Выводим все транзакции.")

    search_input = input("Программа: Фильтровать по слову в описании? Да/Нет\n> ").strip().lower()
    final_list = sorted_result

    if search_input in ("да", "д", "yes", "y"):
        search_term = input("Программа: Введите слово для поиска в описании:\n> ").strip()
        final_list = process_bank_search(sorted_result, search_term)
        if not final_list:
            print("Ничего не найдено по вашему запросу.")
            return
    else:
        print("Поиск по описанию отключён.")

    # Генерация замаскированных данных для вывода
    masked_list = [mask_sensitive_info(tx) for tx in final_list]

    print("\n=== РЕЗУЛЬТАТЫ ===")
    for i, tx in enumerate(masked_list, start=1):
        print_transaction(tx, i)

    print_category_stats(final_list)


if __name__ == "__main__":
    main()
