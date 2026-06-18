import re
from datetime import datetime

from masks import get_mask_account, get_mask_card_number


def mask_account_card(input_string: str) -> str:
    """Обрабатывает строку с типами и номерами карт/счетов, возвращает строку с маскированными номерами."""
    # Находим все последовательности цифр с их позициями
    number_matches = list(re.finditer(r"\d+", input_string))

    if not number_matches:
        return "В строке не найден номер карты или счёта!!!!"

    # Создаём копию строки для последовательной замены
    result = input_string

    # Обрабатываем с конца, чтобы не сбивать позиции при замене
    for match in reversed(number_matches):
        full_number = match.group()
        start_pos = match.start()

        # Определяем тип по тексту перед номером
        context_before = input_string[:start_pos].lower()

        if "счёт" in context_before or "счет" in context_before or "account" in context_before:
            masked_number = get_mask_account(full_number)
        else:
            masked_number = get_mask_card_number(full_number)

        # Точная замена по индексам — заменяем только найденный номер
        result = result[: match.start()] + masked_number + result[match.end() :]

    return result


def get_date(date_string: str) -> str:
    """Преобразует строку с датой из формата 'YYYY-MM-DDTHH:MM:SS.ffffff'
    в формат 'ДД.ММ.ГГГГ'."""
    try:
        # Парсим входную строку в объект datetime
        dt = datetime.fromisoformat(date_string)
        # Форматируем в нужный формат (день, месяц, год с ведущими нулями)
        formatted_date = dt.strftime("%d.%m.%Y")
        return formatted_date
    except ValueError as e:
        return f"Ошибка формата даты: {e}"
