import logging

logger = logging.getLogger(__name__)


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

    masked = f"{card_number[:4]} **** **** {card_number[-4:]}"
    logger.debug("Замаскирован номер карты: %s", masked)
    return masked