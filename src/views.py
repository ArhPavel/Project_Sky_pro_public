# src/views.py

from datetime import datetime
import json
import logging
import pandas as pd
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def get_greeting(current_time: datetime) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def filter_operations_by_date(operations: List[Dict[str, Any]], date_to: datetime) -> List[Dict[str, Any]]:
    """Фильтрует транзакции в диапазоне с 1-го числа месяца входящей даты по саму входящую дату."""
    date_from = datetime(date_to.year, date_to.month, 1, 0, 0, 0)
    filtered = []
    for op in operations:
        op_date_str = op.get("Дата операции")
        if not op_date_str or pd.isna(op_date_str):
            continue
        try:
            if isinstance(op_date_str, str):
                op_date = datetime.strptime(op_date_str, "%d.%m.%Y %H:%M:%S")
            else:
                op_date = pd.to_datetime(op_date_str).to_pydatetime()
            if date_from <= op_date <= date_to:
                filtered.append(op)
        except Exception:
            continue
    return filtered


def calculate_cards_info(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Рассчитывает агрегированные расходы и кэшбэк по каждой карте."""
    cards_data = {}
    for op in operations:
        card_number = op.get("Номер карты")
        if not card_number or pd.isna(card_number):
            continue
        card_str = str(card_number).strip().replace("*", "")
        amount = op.get("Сумma операции", op.get("Сумма операции", 0))
        if amount < 0:
            if card_str not in cards_data:
                cards_data[card_str] = 0.0
            cards_data[card_str] += abs(amount)

    return [
        {"last_digits": card, "total_spent": round(spent, 2), "cashback": round((spent // 100) * 1, 2)}
        for card, spent in cards_data.items()
    ]


def get_top_transactions(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Возвращает топ-5 транзакций по модулю суммы."""
    sorted_ops = sorted(operations, key=lambda x: abs(x.get("Сумма операции", 0)), reverse=True)
    top_5 = []
    for op in sorted_ops[:5]:
        op_date = op.get("Дата операции")
        date_str = op_date.split()[0] if isinstance(op_date, str) else pd.to_datetime(op_date).strftime("%d.%m.%Y")
        top_5.append({
            "date": date_str,
            "amount": round(op.get("Сумма операции", 0), 2),
            "category": str(op.get("Категория", "Разное")),
            "description": str(op.get("Описание", ""))
        })
    return top_5


def generate_main_page_data(
        date_time_str: str, operations: List[Dict[str, Any]],
        currency_rates: List[Dict[str, Any]], stock_prices: List[Dict[str, Any]]
) -> str:
    """Главная функция формирования JSON-ответа для веб-страницы."""
    input_dt = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    filtered_ops = filter_operations_by_date(operations, input_dt)

    return json.dumps({
        "greeting": get_greeting(input_dt),
        "cards": calculate_cards_info(filtered_ops),
        "top_transactions": get_top_transactions(filtered_ops),
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }, ensure_ascii=False, indent=2)
