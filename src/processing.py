from datetime import datetime
from typing import Any, Dict, List

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def filter_by_state(data_list: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрует данные по указанному статусу."""
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
    """Сортирует данные по дате. Невалидные/отсутствующие даты идут в конец."""
    valid = []
    invalid = []

    for item in data_list:
        date_value = item.get("date")
        if _is_valid_iso_date(date_value):
            valid.append(item)
        else:
            invalid.append(item)

    # Сортируем только валидные по строке даты
    valid_sorted = sorted(valid, key=lambda x: x["date"], reverse=reverse_order)

    return valid_sorted + invalid
