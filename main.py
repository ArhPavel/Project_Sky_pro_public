import logging
from pathlib import Path
# from src.masks import get_mask_card_number
# from src.Utils import load_transactions

#  Создаём папку logs
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Настраиваем корневой логгер
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# Очищаем старые хендлеры, чтобы не дублировать при рестарте
if root_logger.handlers:
    root_logger.handlers.clear()

#  FileHandler с режимом 'w' — перезаписывает файл при каждом запуске
file_handler = logging.FileHandler(logs_dir / "app.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)

root_logger.addHandler(file_handler)

# Проверка лога
# logging.info("Приложение запущено, проверка логирования")

# try:
#     get_mask_card_number("123")  # вызовет ошибку → logger.error в src.masks
# except Exception:
#     pass
#
# result = get_mask_card_number("1111222233334444")
# logging.debug("Успешная маска: %s", result)
#
#
#
# transactions = load_transactions("data/operations.json")
# print(f"Загружено транзакций: {len(transactions)}")
