class CardNumberError(ValueError):
    """Ошибка при некорректном номере карты."""

    pass


class AccountNumberError(ValueError):
    """Ошибка при некорректном номере счёта."""

    pass


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты, оставляя видимыми первые 4 и последние 4 цифры.

    Формат: 1234 **** **** 5678
    """
    if not isinstance(card_number, str):
        raise CardNumberError("Номер карты должен быть строкой.")

    if len(card_number) != 16 or not card_number.isdigit():
        raise CardNumberError("Некорректный номер карты: ожидается 16 цифр.")

    return f"{card_number[:4]} **** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счёта, оставляя видимыми только последние 4 цифры."""
    if not isinstance(account_number, str):
        raise AccountNumberError("Номер счёта должен быть строкой.")

    if len(account_number) != 20 or not account_number.isdigit():
        raise AccountNumberError("Некорректный номер счёта: ожидается 20 цифр.")

    return f"**{account_number[-4:]}"
