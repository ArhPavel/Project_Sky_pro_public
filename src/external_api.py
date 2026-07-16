import os
from typing import Any, Dict, Optional

import requests

API_URL = "https://api.apilayer.com/exchangerates_data/latest"


def get_exchange_rate(base_currency: str, target_currency: str = "RUB") -> Optional[float]:
    """
    Получает текущий курс валюты к RUB через Exchange Rates Data API.

    Возвращает:
        - float: курс (сколько рублей за 1 единицу base_currency)
        - None: если запрос не удался или данных нет
    """
    api_key = os.getenv("EXCHANGE_API_KEY")
    if not api_key:
        return None

    params = {
        "apikey": api_key,
        "base": base_currency,
        "symbols": target_currency,
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()
    except (requests.RequestException, ValueError):
        return None

    rates = data.get("rates", {})
    rate = rates.get(target_currency)
    if rate is None:
        return None

    return float(rate)


def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли."""

    amount = transaction.get("amount", 0)
    currency = (transaction.get("currency") or "").upper()

    if currency == "RUB":
        return float(amount)

    if currency in ("USD", "EUR"):
        rate = get_exchange_rate(currency, "RUB")
        if rate is not None:
            return float(amount * rate)

    return 0.0
