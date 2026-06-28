import pytest
from src.masks import (get_mask_card_number, get_mask_account, CardNumberError, AccountNumberError)


@pytest.fixture
def valid_card_cases():
    """Пары: (входной номер, ожидаемая маска)."""
    return [
        ("1234567890123456", "1234 **** **** 3456"),
        ("0000111122223333", "0000 **** **** 3333"),
        ("9999888877776666", "9999 **** **** 6666"),
    ]


@pytest.fixture
def valid_account_cases():
    """Пары: (входной счёт, ожидаемая маска)."""
    # Подстраивай под реальную логику get_mask_account: если она маскирует всё кроме последних 4 — так и оставь.
    return [
        ("11112222333344445555", "**5555"),
        ("00009999888877776666", "**6666"),
    ]


class TestCardMask:
    def test_valid_cards(self, valid_card_cases):
        for card, expected in valid_card_cases:
            assert get_mask_card_number(card) == expected

    @pytest.mark.parametrize("invalid_card",["1234", "123456789012345", "12345678901234567", "", "12a4567890123456", "12 45 67 89",
None,  ], )
    def test_invalid_cards_raise(self, invalid_card):
        with pytest.raises(CardNumberError):
            get_mask_card_number(invalid_card)


class TestAccountMask:
    def test_valid_accounts(self, valid_account_cases):
        for account, expected in valid_account_cases:
            assert get_mask_account(account) == expected

    @pytest.mark.parametrize("invalid_account", ["1234", "1", "", "12a34567890", None, ], )
    def test_invalid_accounts_raise(self, invalid_account):
        with pytest.raises(AccountNumberError):
            get_mask_account(invalid_account)