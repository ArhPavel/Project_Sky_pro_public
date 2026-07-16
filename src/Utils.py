import json
import os
from typing import Any, Dict, List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из JSON-файла.

    Возвращает пустой список, если:
      - файл не найден,
      - файл пустой,
      - содержимое не является списком,
      - JSON невалиден.
    """

    if not os.path.isfile(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError:

        return []

    if not text.strip():
        return []

    try:
        data = json.loads(text)
    except json.JSONDecodeError:

        return []

    if not isinstance(data, list):
        return []

    result: List[Dict[str, Any]] = []
    for item in data:
        if isinstance(item, dict):
            result.append(item)

    return result
