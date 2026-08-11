# src/processing.py
import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List

# Поддерживаем базовый ISO формат и формат с миллисекундами
DATE_FORMATS = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"]


def filter_by_state(data_list: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрует список транзакций по полю 'state'."""
    return [item for item in data_list if str(item.get("state") or item.get("status", "")).upper() == state.upper()]


def _is_valid_iso_date(date_str: Any) -> bool:
    if not isinstance(date_str, str):
        return False

    clean_date = date_str[:-1] if date_str.endswith("Z") else date_str
    for fmt in DATE_FORMATS:
        try:
            datetime.strptime(clean_date, fmt)
            return True
        except ValueError:
            continue
    return False


def sort_by_date(data_list: List[Dict[str, Any]], reverse_order: bool = True) -> List[Dict[str, Any]]:
    """Сортирует транзакции по полю 'date' в формате ISO."""
    valid = []
    invalid = []

    for item in data_list:
        date_value = item.get("date")
        if _is_valid_iso_date(date_value):
            valid.append(item)
        else:
            invalid.append(item)

    valid_sorted = sorted(valid, key=lambda x: x["date"], reverse=reverse_order)
    return valid_sorted + invalid


def count_by_category(transactions: List[Dict[str, Any]]) -> Counter[str]:
    """Подсчитывает количество операций по аналитическому полю или описанию."""
    categories = []
    for t in transactions:
        # Ищем явную категорию, либо пытаемся вытащить её из описания
        cat = t.get("category") or t.get("description") or t.get("operation") or "unknown"
        categories.append(str(cat).split()[0].lower())  # Берем первое слово для красивой группировки
    return Counter(categories)


def filter_rub_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Оставляет только транзакции с валютой RUB."""
    return [
        t
        for t in transactions
        if (
            str(t.get("currency_code") or t.get("currency") or "").upper() == "RUB"
            or str(t.get("operationAmount", {}).get("currency", {}).get("code", "")).upper() == "RUB"
        )
    ]


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """Фильтрует транзакции по регулярному выражению в описании."""
    try:
        pattern = re.compile(search, re.IGNORECASE)
    except re.error:
        print("Ошибка в регулярном выражении")
        return []

    return [
        tx
        for tx in data
        if pattern.search(str(tx.get("description", ""))) or pattern.search(str(tx.get("operation", "")))
    ]


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество операций по заданным ключевым словам."""
    result = {category: 0 for category in categories}
    for tx in data:
        description = str(tx.get("description", "")).lower()
        operation = str(tx.get("operation", "")).lower()
        for category in categories:
            if category.lower() in description or category.lower() in operation:
                result[category] += 1
    return result
