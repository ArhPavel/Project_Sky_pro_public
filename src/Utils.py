import json
import logging
import os
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из JSON-файла.

    Возвращает пустой список, если:
      - файл не найден,
      - файл пустой,
      - содержимое не является списком,
      - JSON невалиден.
    """
    logger.debug("Попытка загрузки транзакций из файла: %s", file_path)

    if not os.path.isfile(file_path):
        logger.error("Файл транзакций не найден: %s", file_path)
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        logger.error("Ошибка чтения файла транзакций %s: %s", file_path, e)
        return []

    if not text.strip():
        logger.warning("Файл транзакций пуст или содержит только пробельные символы: %s", file_path)
        return []

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        logger.error("Невалидный JSON в файле %s: %s", file_path, e)
        return []

    if not isinstance(data, list):
        logger.error(
            "Содержимое файла %s не является списком (получен тип: %s)",
            file_path,
            type(data).__name__,
        )
        return []

    result: List[Dict[str, Any]] = [item for item in data if isinstance(item, dict)]
    count_skipped = len(data) - len(result)

    if count_skipped > 0:
        logger.warning(
            "В файле %s пропущено %d элементов, которые не являются словарями",
            file_path,
            count_skipped,
        )

    logger.info("Успешно загружено %d транзакций из %s", len(result), file_path)
    return result
