import logging
import os

module_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(module_dir)

logs_dir = os.path.join(project_root, "logs")


if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

logger = logging.getLogger(__name__)

if not logger.handlers:
    log_file_path = os.path.join(logs_dir, "masks.log")
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)-8s | %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

logger.info("masks.py: логгер настроен, путь: %s", logs_dir)


class CardNumberError(ValueError):
    """Ошибка при некорректном номере карты."""

    pass


def get_mask_card_number(card_number: str) -> str:
    if not isinstance(card_number, str):
        logger.error("Номер карты должен быть строкой. Получено: %r", card_number)
        raise CardNumberError("Номер карты должен быть строкой.")

    if len(card_number) != 16 or not card_number.isdigit():
        logger.error(
            "Некорректный номер карты: ожидается 16 цифр. Получено: %r (длина %d)",
            card_number,
            len(card_number) if isinstance(card_number, str) else 0,
        )
        raise CardNumberError("Некорректный номер карты: ожидается 16 цифр.")

    # Теперь эта ветка достижима только при корректных данных
    masked = f"{card_number[:4]} **** **** {card_number[-4:]}"
    logger.debug("Замаскирован номер карты: %s", masked)  # <-- теперь достижимо
    return masked
