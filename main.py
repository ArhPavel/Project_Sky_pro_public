import logging
from src.Utils import logger as utils_logger
from src.masks import logger as masks_logger

print("=== Проверка логгеров ===")
print("utils_logger.level:", utils_logger.getEffectiveLevel())
print("utils_logger.handlers:", utils_logger.handlers)
print("masks_logger.level:", masks_logger.getEffectiveLevel())
print("masks_logger.handlers:", masks_logger.handlers)

# Для каждого хендлера выведем его уровень
for h in utils_logger.handlers:
    print("  utils handler level:", h.level, h)
for h in masks_logger.handlers:
    print("  masks handler level:", h.level, h)