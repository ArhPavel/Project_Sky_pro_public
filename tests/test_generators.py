#filter_by_currency -тестирование
import pytest
from src.generators import filter_by_currency


@pytest.fixture
def transactions():
    return [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 2, "amount": 200, "currency": "EUR"},
        {"id": 3, "amount": 150, "currency": "USD"},
        {"id": 4, "amount": 300},  # нет поля currency
        {"id": 5, "amount": 400, "currency": None},  # currency = None
    ]


def test_filter_by_currency_returns_iterator(transactions):
    result = filter_by_currency(transactions, "USD")
    assert hasattr(result, "__iter__")
    assert hasattr(result, "__next__")


def test_filter_by_currency_filters_correctly(transactions):
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 2
    ids = [t["id"] for t in usd_transactions]
    assert ids == [1, 3]


def test_filter_by_currency_no_matches(transactions):
    no_match = list(filter_by_currency(transactions, "JPY"))
    assert no_match == []


def test_filter_by_currency_empty_list():
    result = list(filter_by_currency([], "USD"))
    assert result == []

#transaction_descriptions - тестирование
from typing import List, Dict, Any
from src.generators import transaction_descriptions

@pytest.mark.parametrize(
    "transactions,expected",[
        # Обычный случай: operation_type задан
        ([{"operation_type": "Перевод организации"},
                {"operation_type": "Перевод со счета на счет"},],
            [
                "Перевод организации",
                "Перевод со счета на счет",
            ],),
        # Пустая строка в operation_type — должна считаться «неизвестной»
        ([{"operation_type": ""}, {"operation_type": "Перевод с карты на карту"},],
            [
                "Неизвестная операция",
                "Перевод с карты на карту",
            ],),
        # Нет operation_type, есть type — должен использоваться type
        ([{"type": "Платеж поставщику"},{"type": ""},  # type пустой — тоже «неизвестная»
            ],[
                "Платеж поставщику",
                "Неизвестная операция",
            ],
        ),
        # Смешанный случай: часть через operation_type, часть через type, часть без обоих
        ([ {"operation_type": "Перевод организации"},
                {"type": "Платеж поставщику"},
                {},
                {"operation_type": "", "type": ""},
            ],
            [
                "Перевод организации",
                "Платеж поставщику",
                "Неизвестная операция",
                "Неизвестная операция",
            ],
        ),
        # Пустой список
        ([], []),
    ],
)
def test_transaction_descriptions(transactions: List[Dict[str, Any]], expected: List[str]) -> None:
    result = list(transaction_descriptions(transactions))
    assert result == expected
def test_transaction_descriptions_as_generator() -> None:
    transactions = [
        {"operation_type": "Перевод организации"},
        {"operation_type": "Перевод со счета на счет"},
        {"operation_type": "Перевод с карты на карту"},
    ]

    descriptions = transaction_descriptions(transactions)
    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод с карты на карту"

    # Проверка, что после исчерпания будет StopIteration
    with pytest.raises(StopIteration):
        next(descriptions)


#card_number_generator -тестирование
from src.generators import card_number_generator


@pytest.mark.parametrize(
    "start,end,expected",
    [
        # Маленькие числа — проверяем, что докидываются нули
        (1, 3, [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
        ]),
        # Числа ровно по 4/8/12 цифр — проверяем разбиение на группы
        (1234, 1234, [
            "0000 0000 0000 1234",
        ]),
        (12345678, 12345678, [
            "0000 0000 1234 5678",
        ]),
        (123456789012, 123456789012, [
            "0000 1234 5678 9012",
        ]),
        # «Круглые» значения и переход через разряд
        (9999999999999998, 9999999999999999, [
            "9999 9999 9999 9998",
            "9999 9999 9999 9999",
        ]),
    ],
)
def test_card_number_generator_correct_output(start: int, end: int, expected: list[str]) -> None:
    result = list(card_number_generator(start, end))
    assert result == expected


def test_card_number_generator_invalid_start_raises() -> None:
    with pytest.raises(ValueError):
        list(card_number_generator(0, 10))

    with pytest.raises(ValueError):
        list(card_number_generator(-5, 10))


def test_card_number_generator_invalid_end_raises() -> None:
    max_allowed = 9999_9999_9999_9999
    with pytest.raises(ValueError):
        list(card_number_generator(max_allowed, max_allowed + 1))