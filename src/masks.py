import logging
import os

module_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(module_dir)
logs_dir = os.path.join(project_root, "logs")

os.makedirs(logs_dir, exist_ok=True)

logger = logging.getLogger(__name__)

if not logger.handlers:
    log_file_path = os.path.join(logs_dir, "masks.log")
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)-8s | %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)


class CardNumberError(ValueError):
    """Ошибка при некорректном номере карты или счёта."""

    pass


def get_mask_card_number(card_number: str) -> str:
    if not isinstance(card_number, str):
        logger.error("Номер карты должен быть строкой. Получено: %r", card_number)
        raise CardNumberError("Номер карты должен быть строкой.")

    clean_number = card_number.replace(" ", "").replace("-", "")

    if len(clean_number) != 16 or not clean_number.isdigit():
        logger.error(
            "Некорректный номер карты: ожидается 16 цифр. Получено: %r (длина %d)",
            card_number,
            len(clean_number),
        )
        raise CardNumberError("Некорректный номер карты: ожидается 16 цифр.")

    masked = f"{clean_number[:4]} **** **** {clean_number[-4:]}"
    logger.debug("Замаскирован номер карты: %s", masked)
    return masked


def get_mask_account(account_number: str) -> str:
    if not isinstance(account_number, str):
        logger.error("Номер счёта должен быть строкой. Получено: %r", account_number)
        raise CardNumberError("Номер счёта должен быть строкой.")

    clean_account = account_number.replace(" ", "").replace("-", "")

    if not clean_account.isdigit():
        logger.error("Номер счёта содержит недопустимые символы: %r", account_number)
        raise CardNumberError("Номер счёта должен содержать только цифры.")

    if len(clean_account) < 4:
        logger.error(
            "Слишком короткий номер счёта: %r (требуется минимум 4 цифры)",
            account_number,
        )
        raise CardNumberError("Слишком короткий номер счёта (требуется минимум 4 цифры).")

    last_four = clean_account[-4:]
    result = f"**{last_four}"

    logger.debug(
        "Замаскирован номер счёта: исходный=%s, результат=%s",
        account_number,
        result,
    )
    return result
