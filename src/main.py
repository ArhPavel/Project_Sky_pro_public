# src/main

import logging
import pandas as pd
from src.utils import read_excel_operations, load_user_settings, get_currency_rates, get_stock_prices
from src.views import generate_main_page_data
from src.services import get_cashback_by_categories, simple_search, search_person_transfers
from src.reports import spending_by_category, spending_by_weekday

# Настройка глобального форматирования логов проекта
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("main")


def main():
    logger.info("Запуск основного процесса выполнения курсового проекта")

    # Пути к файлам в соответствии со структурой проекта
    excel_path = "data/operations.xlsx"
    settings_path = "user_settings.json"

    # Шаг 1: Чтение внешних источников данных (Ввод-вывод)
    raw_ops = read_excel_operations(excel_path)
    settings = load_user_settings(settings_path)

    # Запрашиваем информацию из внешних API
    currencies = get_currency_rates(settings.get("user_currencies", ["USD", "EUR"]))
    stocks = get_stock_prices(settings.get("user_stocks", ["AAPL", "AMZN"]))

    # Целевая тестовая дата для проверки работы главной веб-страницы
    target_date_str = "2020-05-20 14:30:00"

    print("\n" + "=" * 50)
    print(" РЕЗУЛЬТАТ РАБОТЫ СТРАНИЦЫ «ГЛАВНАЯ» (JSON):")
    print("=" * 50)
    main_page_json = generate_main_page_data(target_date_str, raw_ops, currencies, stocks)
    print(main_page_json)

    print("\n" + "=" * 50)
    print(" РЕЗУЛЬТАТ РАБОТЫ СЕРВИСА КЭШБЭКА:")
    print("=" * 50)
    cashback_json = get_cashback_by_categories(raw_ops, 2020, 5)
    print(cashback_json)

    print("\n" + "=" * 50)
    print(" РЕЗУЛЬТАТ РАБОТЫ СЕРВИСА ПОИСКА ФИЗЛИЦ:")
    print("=" * 50)
    transfers_json = search_person_transfers(raw_ops)
    print(transfers_json)

    # Шаг 2: Формирование отчетов через pandas DataFrame
    if raw_ops:
        df_ops = pd.DataFrame(raw_ops)

        logger.info("Генерация отчета по тратам в категории...")
        spending_by_category(df_ops, "Супермаркеты", "20.05.2020")

        logger.info("Генерация отчета по дням недели...")
        spending_by_weekday(df_ops, "20.05.2020")

    logger.info("Программа успешно завершила работу.")


if __name__ == "__main__":
    main()
