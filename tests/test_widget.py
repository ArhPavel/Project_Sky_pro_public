import pytest
import re
from datetime import datetime
from src.masks import get_mask_account, get_mask_card_number


# --- Функции (вместо src/utils.py) ---

def mask_account_card(input_string: str) -> str:
    number_matches = list(re.finditer(r"\d+", input_string))

    if not number_matches:
        return "В строке не найден номер карты или счёта!!!!"

    result = input_string

    for match in reversed(number_matches):
        full_number = match.group()
        start_pos = match.start()

        context_before = input_string[:start_pos].lower()

        if "счёт" in context_before or "счет" in context_before or "account" in context_before:
            masked_number = get_mask_account(full_number)
        else:
            masked_number = get_mask_card_number(full_number)

        result = result[:start_pos] + masked_number + result[match.end():]

    return result


def get_date(date_string: str) -> str:
    try:
        dt = datetime.fromisoformat(date_string)
        return dt.strftime("%d.%m.%Y")
    except ValueError as e:
        return f"Ошибка формата даты: {e}"


# --- Тесты с фикстурами ---

@pytest.fixture
def valid_iso_dates():
    return [ ("2026-06-10T12:00:00.123456", "10.06.2026"), ("2026-01-01T00:00:00", "01.01.2026"), ("2026-05-03T09:15:00.000000", "03.05.2026"), ]


@pytest.fixture
def invalid_date_inputs():
    return ["10.06.2026", "", "not-a-date", "2026-13-01T00:00:00", ]


class TestGetDate:
    def test_valid_iso_formats(self, valid_iso_dates):
        for input_date, expected in valid_iso_dates:
            assert get_date(input_date) == expected

    def test_invalid_formats_return_error_message(self, invalid_date_inputs):
        for invalid_input in invalid_date_inputs:
            result = get_date(invalid_input)
            assert result.startswith("Ошибка формата даты:")


class TestMaskAccountCard:
    @pytest.fixture
    def mask_cases(self):
        return [ ( "Операция по карте 1234567890123456 завершена", "Операция по карте 1234 **** **** 3456 завершена" ), (
 "Перевод на счёт 11112222333344445555 выполнен", "Перевод на счёт **5555 выполнен" ),]

    @pytest.fixture
    def edge_cases(self):
        return [ ("В строке нет никаких номеров", "В строке не найден номер карты или счёта!!!!"), ("Платёж на СЧЁТ 11112222333344445555", "Платёж на СЧЁТ **5555"), ]
    def test_standard_mask_cases(self, mask_cases):
        for input_str, expected in mask_cases:
            assert mask_account_card(input_str) == expected

    def test_edge_cases(self, edge_cases):
        for input_str, expected in edge_cases:
            assert mask_account_card(input_str) == expected