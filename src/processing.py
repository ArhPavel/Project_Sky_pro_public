from typing import List, Dict, Any


def filter_by_state(data_list: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует данные по указанному статусу.

    Args:
        data_list: Список словарей с данными для фильтрации.
        state: Статус для фильтрации (по умолчанию "EXECUTED").

    Returns:
        Список элементов, соответствующих указанному статусу.
    """
    return [item for item in data_list if item.get("state") == state]


def sort_by_date(data_list: List[Dict[str, Any]], reverse_order: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует данные по дате.

    Args:
        data_list: Список словарей с данными для сортировки.
        reverse_order: Флаг сортировки в обратном порядке (по умолчанию True).

    Returns:
        Отсортированный список элементов.
    """
    return sorted(data_list, key=lambda item: item.get("date", ""), reverse=reverse_order)
