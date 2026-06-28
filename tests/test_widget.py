import pytest

# Исправленный импорт: src, а не scr
from src.widget import mask_account_card, get_date


def test_mask_account_card_empty_string():
    assert mask_account_card("") == "В строке не найден номер карты или счёта!!!!"


def test_mask_account_card_no_numbers():
    assert mask_account_card("Текст без цифр") == "В строке не найден номер карты или счёта!!!!"


def test_mask_account_card_single_card():
    text = "Карта 1234567890123456"
    result = mask_account_card(text)
    # Проверяем, что маска применилась и видны первые и последние 4 цифры
    assert "1234" in result
    assert "3456" in result
    assert "****" in result


def test_mask_account_card_single_account():
    text = "Счёт 98765432109876543210"
    result = mask_account_card(text)
    # Маска счёта должна оставить последние 4 цифры и скрыть остальное
    assert result != text
    assert "3210" in result


def test_mask_account_card_mixed_types():
    text = "Карта: 1111222233334444, счёт: 99998888777766665555"
    result = mask_account_card(text)
    assert "1111 **** **** 4444" in result or "1111**** ****4444" in result
    assert "5555" in result  # последние 4 счёта должны остаться


def test_mask_account_card_multiple_numbers():
    text = "Номера: 1111222233334444 5555666677778888"
    result = mask_account_card(text)
    assert result.count("****") >= 2


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("2026-06-28T12:34:56.123456", "28.06.2026"),
        ("2026-06-28T12:34:56", "28.06.2026"),
        ("2026-01-01T00:00:00", "01.01.2026"),
        ("2026-12-31T23:59:59.999999", "31.12.2026"),
    ],
)
def test_get_date_valid(input_str: str, expected: str):
    assert get_date(input_str) == expected