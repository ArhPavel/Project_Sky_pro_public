import os
from typing import Any, Dict, List, Optional

from src.masks import get_mask_account, get_mask_card_number
from src.processing import count_by_category, filter_by_state, filter_rub_transactions, sort_by_date
from src.transaction_reader import load_csv_transactions, load_excel_transactions, load_json_transactions


# НАСТРОЙКА ПУТЕЙ (ОДИН РАЗ В ТОЧКЕ ВХОДА)

project_root = os.getcwd()
data_dir = os.path.join(project_root, "data")

csv_path = os.path.join(data_dir, "transactions.csv")
excel_path = os.path.join(data_dir, "transactions_excel.xlsx")
json_path = os.path.join(data_dir, "transactions.json")



# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ



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
        val = amount

    if currency == "RUB":
        return f"{val:,.2f} руб."
    elif currency == "USD":
        return f"{val:,.2f} USD"
    elif currency == "EUR":
        return f"{val:,.2f} EUR"
    else:
        return f"{val:,.2f}"


def mask_sensitive_info(transaction: Dict[Any, Any]) -> Dict[str, Any]:
    # Приводим все ключи к str, чтобы дальше не было проблем с типами
    tx = {str(k): v for k, v in transaction.items()}

    card = tx.get("card_number")
    account = tx.get("account")

    masked_card = None
    masked_account = None

    if card:
        try:
            masked_card = get_mask_card_number(str(card))
        except Exception:
            masked_card = "[ошибка маскирования]"

    if account:
        try:
            masked_account = get_mask_account(str(account))
        except Exception:
            masked_account = "[ошибка маскирования]"

    tx["_masked_card"] = masked_card
    tx["_masked_account"] = masked_account
    return tx


def print_transaction(tx: Dict[str, Any], idx: int) -> None:
    date_str = tx.get("date", "?")
    description = tx.get("description", tx.get("operation", "Неизвестная операция"))
    amount = tx.get("amount")
    currency = tx.get("currency", "").upper()
    card = tx.get("_masked_card")
    account = tx.get("_masked_account")

    print(f"{date_str} {description}")

    if account:
        print(f"Счет {account}")
    elif card:
        print(f"Карта {card}")

    amount_str = format_currency_amount(amount, currency)
    print(f"Сумма: {amount_str}")
    print()  # пустая строка между транзакциями


def print_category_stats(transactions: List[Dict[str, Any]]) -> None:
    """Выводит статистику по категориям транзакций."""
    counter = count_by_category(transactions)

    if not counter:
        print("Статистика по категориям недоступна (нет транзакций).")
        return

    print("📊 Статистика по категориям:")
    total = sum(counter.values())
    for category, count in counter.most_common():
        percent = (count / total) * 100
        print(f" {category}: {count} шт. ({percent:.1f}%)")
    print()



# ОСНОВНАЯ ЛОГИКА (MAIN)



def main() -> None:
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ").strip()

    all_transactions: List[Dict[str, Any]] = []

    # Безопасное получение данных: если функция вернёт не list, делаем пустой список
    raw_data: Any = []
    if choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        raw_data = load_json_transactions(json_path)
    elif choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        raw_data = load_csv_transactions(csv_path)
    elif choice == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
        raw_data = load_excel_transactions(excel_path)
    else:
        print("Программа: Неверный выбор. Завершение работы.")
        return

    # Гарантируем, что у нас именно список
    if isinstance(raw_data, list):
        all_transactions = raw_data
    else:
        all_transactions = []
        print("⚠️ Предупреждение: функция загрузки вернула не список. Данные не загружены.")
        return

    if not all_transactions:
        print("Программа: Не найдено ни одной транзакции в выбранном файле.")
        return

    # --- Фильтрация по статусу ---
    target_status = get_valid_status()
    filtered = filter_by_state(all_transactions, state=target_status)

    if not filtered:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    # --- Сортировка по дате ---
    sort_date_input = input("Программа: Отсортировать операции по дате? Да/Нет\n> ").strip().lower()
    sorted_result = filtered

    if sort_date_input in ("да", "д", "yes", "y"):
        order_input = input("Программа: Отсортировать по возрастанию или по убыванию?\n> ").strip().lower()
        reverse_order = order_input in ("убыванию", "по убыванию", "desc", "down")
        sorted_result = sort_by_date(filtered, reverse_order=reverse_order)

    # --- Только рублёвые транзакции (через готовую функцию) ---
    rub_only_input = input("Программа: Выводить только рублёвые транзакции? Да/Нет\n> ").strip().lower()
    rub_only = rub_only_input in ("да", "д", "yes", "y")

    if rub_only:
        sorted_result = filter_rub_transactions(sorted_result)
        print("✅ Отфильтрованы только RUB транзакции.")
    else:
        print("✅ Выводим все транзакции.")

    # --- Поиск по слову в описании ---
    search_input = (
        input("Программа: Отфильтровать список транзакций по определённому слову в описании? Да/Нет\n> ")
        .strip()
        .lower()
    )
    search_term = ""
    if search_input in ("да", "д", "yes", "y"):
        search_term = input("Программа: Введите слово для поиска в описании:\n> ").strip().lower()

    if search_term:
        sorted_result = [
            tx
            for tx in sorted_result
            if search_term in str(tx.get("description", "")).lower()
            or search_term in str(tx.get("operation", "")).lower()
        ]

    # --- Маскирование чувствительных данных ---
    masked_list = [mask_sensitive_info(tx) for tx in sorted_result]

    # --- Вывод итогового списка ---
    print("Программа: Распечатываю итоговый список транзакций...\n")
    print(f"Всего банковских операций в выборке: {len(masked_list)}\n")

    if len(masked_list) == 0:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    for i, tx in enumerate(masked_list):
        print_transaction(tx, i + 1)

    # --- Статистика по категориям ---
    print_category_stats(masked_list)


if __name__ == "__main__":
    main()
