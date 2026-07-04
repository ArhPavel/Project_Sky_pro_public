from typing import Any, Dict, Iterable, Iterator


def filter_by_currency(transactions: Iterable[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """Возвращает итератор по транзакции с указанной валютой
    transactions: список словарей, каждый словарь - транзакция
    currency: строка с кодом валюты (например, 'USD')"""
    for transaction in transactions:
        if transaction.get("currency") == currency:
            yield transaction


def transaction_descriptions(transactions: Iterable[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который по очереди возвращает описание операции."""
    for t in transactions:
        op_type = t.get("operation_type")
        if not op_type and op_type != "":
            op_type = t.get("type")

        # Если всё ещё нет значения или это пустая строка — заглушка
        if op_type == "" or op_type is None:
            yield "Неизвестная операция"
        else:
            yield str(op_type)


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.
    Принимает диапазон целых чисел (от 1 до 9999_9999_9999_9999).
    Выдаёт строки вида "1234 5678 9012 3456"""

    if not (1 <= start <= end <= 9999_9999_9999_9999):
        raise ValueError("Неверный диапазон")

    for number in range(start, end + 1):
        s = str(number)
        # Добиваем нулями спереди, пока длина не станет 16
        while len(s) < 16:
            s = "0" + s

        # Просто берём куски по 4 символа
        part1 = s[0:4]
        part2 = s[4:8]
        part3 = s[8:12]
        part4 = s[12:16]

        yield f"{part1} {part2} {part3} {part4}"
