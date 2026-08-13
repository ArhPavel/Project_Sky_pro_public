#src_services.py

from datetime import datetime
import json
import logging
import re
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def get_cashback_by_categories(data: List[Dict[str, Any]], year: int, month: int) -> str:
    """Анализирует потенциальный кешбэк (1%) по категориям за определенный год и месяц."""
    logger.info(f"Запуск анализа кешбэка за {month:02d}.{year}")

    def is_target_period(op: Dict[str, Any]) -> bool:
        date_str = op.get("Дата операции")
        if not date_str or not isinstance(date_str, str):
            return False
        try:
            op_date = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
            return op_date.year == year and op_date.month == month
        except ValueError:
            return False

    filtered_ops = list(filter(is_target_period, data))
    categories_cashback = {}
    for op in filtered_ops:
        category = op.get("Категория")
        amount = op.get("Сумма операции", 0)
        if category and isinstance(amount, (int, float)) and amount < 0:
            cat_str = str(category).strip()
            categories_cashback[cat_str] = categories_cashback.get(cat_str, 0.0) + (abs(amount) * 0.01)

    final_analysis = {cat: round(cash) for cat, cash in categories_cashback.items() if cash > 0}
    return json.dumps(final_analysis, ensure_ascii=False, indent=2)


def simple_search(data: List[Dict[str, Any]], search_query: str) -> str:
    """Регистронезависимый поиск транзакций по совпадению строки в Описании или Категории."""
    logger.info(f"Запуск простого поиска по запросу: '{search_query}'")
    query_lower = search_query.lower()
    found_ops = list(
        filter(
            lambda op: query_lower in str(op.get("Описание", "")).lower()
            or query_lower in str(op.get("Категория", "")).lower(), data
        )
    )
    return json.dumps(found_ops, ensure_ascii=False, indent=2)


def search_person_transfers(data: List[Dict[str, Any]]) -> str:
    """Находит все переводы физическим лицам, используя регулярные выражения."""
    logger.info("Запуск поиска переводов физлицам")
    name_pattern = re.compile(r"\b[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.")

    def is_person_transfer(op: Dict[str, Any]) -> bool:
        category = str(op.get("Категория", "")).strip()
        description = str(op.get("Описание", "")).strip()
        if category == "Переводы":
            return bool(name_pattern.search(description))
        return False

    matching_transfers = list(filter(is_person_transfer, data))
    result_list = [
        {
            "date": op.get("Дата операции"),
            "amount": op.get("Сумма операции"),
            "category": op.get("Категория"),
            "description": op.get("Описание")
        } for op in matching_transfers
    ]
    return json.dumps(result_list, ensure_ascii=False, indent=2)
