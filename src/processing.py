from collections import Counter
from datetime import datetime
from typing import Any, Dict, List

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def filter_by_state(data_list: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список транзакций по полю 'state'.

    :param data_list: список словарей с транзакциями
    :param state: требуемое значение поля 'state' (сравнение точное)
    :return: отфильтрованный список транзакций
    """
    return [item for item in data_list if item.get("state") == state]


def _is_valid_iso_date(date_str: Any) -> bool:
    if not isinstance(date_str, str):
        return False
    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return True
    except ValueError:
        return False


def sort_by_date(data_list: List[Dict[str, Any]], reverse_order: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по полю 'date' в формате ISO.

    Валидные даты сортируются по убыванию (или возрастанию, если reverse_order=False).
    Записи без даты или с невалидным форматом перемещаются в конец списка.
    Порядок среди невалидных записей не гарантируется.

    :param data_list: список транзакций
    :param reverse_order: если True — сортировка по убыванию даты, иначе по возрастанию
    :return: отсортированный список
    """
    valid = []
    invalid = []

    for item in data_list:
        date_value = item.get("date")
        if _is_valid_iso_date(date_value):
            valid.append(item)
        else:
            invalid.append(item)

    # Сортируем только валидные записи
    valid_sorted = sorted(valid, key=lambda x: x["date"], reverse=reverse_order)
    return valid_sorted + invalid


def count_by_category(transactions: List[Dict[str, Any]]) -> Counter[str]:
    """
    Подсчитывает количество операций по полю 'category'.

    Если поле отсутствует, категория считается как 'unknown'.

    :param transactions: список транзакций
    :return: Counter с количеством по категориям
    """
    categories = [t.get("category", "unknown") for t in transactions]
    return Counter(categories)


def filter_rub_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Оставляет только транзакции с currency_code == 'RUB'."""
    return [t for t in transactions if t.get("currency_code") == "RUB"]
