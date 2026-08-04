import json
import logging
import os
from typing import Any, Dict, List

module_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(module_dir)
logs_dir = os.path.join(project_root, "logs")

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

logger = logging.getLogger(__name__)

if not logger.handlers:
    log_file_path = os.path.join(logs_dir, "utils.log")
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)-8s | %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
logger.info("utils.py: логгер настроен, путь: %s", logs_dir)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Функция загрузки json файла и вывод транзакций."""
    logger.debug("Попытка загрузки транзакций из файла: %s", file_path)

    if not os.path.isfile(file_path):
        # Если файл не найден, возможно, путь относительный и cwd не тот.
        logger.error("Файл транзакций не найден: %s (текущая директория: %s)", file_path, os.getcwd())
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
