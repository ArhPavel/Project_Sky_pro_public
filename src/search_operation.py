import re
from typing import Any, Dict, List


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Ищет операции, в описании (description) которых встречается строка search.
    Поиск регистронезависимый, поддерживает частичные совпадения.

    :param data: список словарей с транзакциями
    :param search: строка поиска (можно использовать спецсимволы regex)
    :return: отфильтрованный список словарей
    """
    if not search:

        return data

    pattern = re.compile(search, re.IGNORECASE)

    result = []
    for row in data:
        description = row.get("description", "") or ""
        if pattern.search(description):
            result.append(row)

    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Считает количество операций по заданным категориям.
    Категория определяется по наличию ключевого слова в поле description.
    Регистр не важен.

    :param data: список словарей с транзакциями
    :param categories: список названий категорий (ключевые слова)
    :return: словарь {категория: количество}
    """
    result = {cat: 0 for cat in categories}

    if not data:
        return result

    for cat in categories:
        pattern = re.compile(re.escape(cat), re.IGNORECASE)

        count = 0
        for row in data:
            description = row.get("description", "") or ""
            if pattern.search(description):
                count += 1

        result[cat] = count

    return result
