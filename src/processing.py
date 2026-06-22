from typing import List, Dict, Any


def filter_by_state(data_list: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрует данные по указанному статусу."""
    return [item for item in data_list if item.get("state") == state]


def sort_by_date(data_list: List[Dict[str, Any]], reverse_order: bool = True) -> List[Dict[str, Any]]:
    """Сортирует данные по дате."""

    def safe_get_date(item: Dict[str, Any]) -> str:
        try:
            date_value = item["date"]
            if isinstance(date_value, str):
                return date_value
            return ""
        except KeyError:
            return ""

    return sorted(data_list, key=safe_get_date, reverse=reverse_order)
