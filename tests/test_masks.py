import pytest

class CardNumberError(ValueError):

    pass

class AccountNumberError(ValueError):

    pass

def get_mask_card_number(card_number: str) -> str:

    if not isinstance(card_number, str):
        raise CardNumberError("Номер карты должен быть строкой.")

    if len(card_number) != 16 or not card_number.isdigit():
        raise CardNumberError("Некорректный номер карты: ожидается 16 цифр.")

    return f"{card_number[:4]} **** **** {card_number[-4:]}"

def get_mask_account(account_number: str) -> str:

    if not isinstance(account_number, str):
        raise AccountNumberError("Номер счёта должен быть строкой.")

    if len(account_number) != 20 or not account_number.isdigit():
        raise AccountNumberError("Некорректный номер счёта: ожидается 20 цифр.")

    return f"**{account_number[-4:]}"
@pytest.fixture
def valid_card_numbers():
    return [
        "1738294051627384",
        "9283746550413221",
    ]

@pytest.fixture
def invalid_card_cases():
    # (входное значение, фрагмент ожидаемого сообщения об ошибке)
    return [
        ("123456789012345", "ожидается 16 цифр"),
        ("12345678901234567", "ожидается 16 цифр"),
        ("1234abcd90123456", "ожидается 16 цифр"),
        (1234567890123456, "должен быть строкой"),
        ("", "ожидается 16 цифр"),
    ]

def test_get_mask_card_number_valid(valid_card_numbers):
    assert get_mask_card_number(valid_card_numbers[0]) == "1738 **** **** 7384"
    assert get_mask_card_number(valid_card_numbers[1]) == "9283 **** **** 3221"

def test_get_mask_card_number_invalid(invalid_card_cases):
    for bad_input, expected_msg_part in invalid_card_cases:
        with pytest.raises(CardNumberError) as exc_info:
            get_mask_card_number(bad_input)
        assert expected_msg_part in str(exc_info.value)