def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты, оставляя видимыми первые 4 и последние 4 цифры."""
    if len(card_number) == 16 and card_number.isdigit():
        masked_card = f"{card_number[:4]} ** **** {card_number[-4:]}"
        return masked_card

    else:
        error_number = "Номер карты указан некорректно!!!!"
        return error_number


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счёта, оставляя видимыми только последние 4 цифры."""
    if len(account_number) == 20 and account_number.isdigit():
        masked_account = f"**{account_number[-4:]}"
        return masked_account

    else:
        error_number = "Номер счёта указан некорректно!!!!"
        return error_number
