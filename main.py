import os
from collections import Counter
from typing import Any, Dict, List, Optional

from src.transaction_reader import load_csv_transactions, load_excel_transactions, load_json_transactions
from src.processing import count_by_category, sort_by_date
from src.masks import get_mask_card_number, get_mask_account

AVAILABLE_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def get_valid_status() -> str:
    while True:
        user_input = input(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        ).strip()
        normalized = user_input.upper()
        if normalized in AVAILABLE_STATUSES:
            print(f'Операции отфильтрованы по статусу "{normalized}"')
            return normalized
        else:
            print(f'Статус операции "{user_input}" недоступен.')


def parse_date_for_sort(date_str: str) -> Optional[str]:
    parts = date_str.strip().split(".")
    if len(parts) == 3:
        day, month, year = parts
        if all(p.isdigit() for p in parts):
            return f"{year}-{month}-{day}"
    return None


def filter_transactions(
    transactions: List[Dict[Any, Any]],
    status: str,
    only_rub: bool,
    search_text: Optional[str],
) -> List[Dict[Any, Any]]:
    result = []
    for t in transactions:
        t_status = str(t.get("status", "")).upper()
        if t_status != status:
            continue

        if only_rub:
            currency = str(t.get("currency", "")).strip().upper()
            if currency != "RUB":
                continue

        if search_text:
            desc = str(t.get("description", "")).lower()
            if search_text.lower() not in desc:
                continue

        result.append(t)
    return result


def sort_transactions(transactions: List[Dict[Any, Any]], ascending: bool) -> List[Dict[Any, Any]]:
    def sort_key(t: Dict[Any, Any]) -> str:
        date_str = str(t.get("date", ""))
        parsed = parse_date_for_sort(date_str)
        if parsed is None:
            return "9999-99-99" if ascending else "0000-00-00"
        return parsed

    return sorted(transactions, key=sort_key, reverse=not ascending)


def format_amount(amount: Any, currency: Any) -> str:
    try:
        amount_val = float(amount) if amount else 0.0
    except (ValueError, TypeError):
        amount_val = 0.0

    currency_val = str(currency).strip().upper() if currency else ""
    if currency_val == "RUB":
        return f"{amount_val:.0f} руб."
    elif currency_val in ("USD", "EUR"):
        return f"{amount_val:.0f} {currency_val}"
    else:
        return f"{amount_val:.2f} {currency_val}"


def mask_sensitive_info(transaction: Dict[str, Any]) -> Dict[str, Any]:
    """Маскирует чувствительные данные в одной транзакции (карта/счёт)."""
    t = transaction.copy()

    card = t.get("card")
    if card:
        try:
            t["card"] = get_mask_card_number(str(card))
        except Exception:
            # Если маска не удалась, оставляем как есть или ставим заглушку
            t["card"] = "**** **** **** ****"

    account = t.get("account")
    if account:
        try:
            t["account"] = get_mask_account(str(account))
        except Exception:
            t["account"] = "********"

    return t


def print_transactions(transactions: List[Dict[Any, Any]]) -> None:
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")
    for t in transactions:
        masked = mask_sensitive_info(t)

        date = masked.get("date", "")
        desc = masked.get("description", "")
        account = masked.get("account", "")
        amount = masked.get("amount")
        currency = masked.get("currency", "")

        formatted_amount = format_amount(amount, currency)

        print(f"{date} {desc}")
        if account:
            print(account)
        print(f"Сумма: {formatted_amount}\n")


def main() -> None:
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input().strip()

    # Вычисляем путь к data относительно расположения main.py
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)  # обычно это корень, если запускаешь python main.py
    data_dir = os.path.join(current_dir, "data")

    file_path = None
    transactions: List[Dict[str, Any]] = []

    if choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        file_path = os.path.join(data_dir, "transactions.json")
        transactions = load_json_transactions(file_path)
    elif choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        file_path = os.path.join(data_dir, "transactions.csv")
        transactions = load_csv_transactions(file_path)
    elif choice == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
        file_path = os.path.join(data_dir, "transactions_excel.xlsx")
        transactions = load_excel_transactions(file_path)
    else:
        print("Программа: Неверный пункт меню. Завершение работы.")
        return

    if not transactions:
        print("Программа: Не удалось загрузить транзакции (файл пуст или не найден).")
        return

    status = get_valid_status()

    sort_choice = input("Программа: Отсортировать операции по дате? Да/Нет\n").strip().lower()
    do_sort = sort_choice in ("да", "д", "yes", "y")

    ascending = True
    if do_sort:
        order_choice = input("Программа: Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        ascending = order_choice in ("по возрастанию", "возрастание", "asc", "a", "да", "д")

    rub_choice = input("Программа: Выводить только рублевые транзакции? Да/Нет\n").strip().lower()
    only_rub = rub_choice in ("да", "д", "yes", "y")

    search_choice = (
        input("Программа: Отфильтровать список транзакций по определённому слову в описании? Да/Нет\n").strip().lower()
    )
    search_text = None
    if search_choice in ("да", "д", "yes", "y"):
        search_text = input("Программа: Введите слово для поиска в описании:\n").strip()

    final_list = filter_transactions(transactions, status, only_rub, search_text)

    if do_sort:
        final_list = sort_transactions(final_list, ascending=ascending)

    print_transactions(final_list)
