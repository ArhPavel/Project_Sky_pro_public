import json
import logging
import os
import pandas as pd
import requests
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def read_excel_operations(file_path: str) -> List[Dict[str, Any]]:
    """Считывает данные о транзакциях из Excel-файла и возвращает список словарей."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(project_root, file_path)

    if not os.path.exists(full_path):
        logger.error(f"Файл {full_path} не найден.")
        return []
    try:
        df = pd.read_excel(full_path)
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel-файла: {e}")
        return []


def load_user_settings(file_path: str) -> Dict[str, Any]:
    """Загружает пользовательские настройки валют и акций из JSON."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(project_root, file_path)

    if not os.path.exists(full_path):
        logger.warning(f"Файл настроек {full_path} не найден. Используются дефолтные значения.")
        return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN"]}
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Ошибка при чтении файла настроек: {e}")
        return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN"]}


def get_currency_rates(currencies: List[str]) -> List[Dict[str, float]]:
    rates_list = []
    try:
        url = "https://api.exchangerate-api.com/v4/latest/RUB"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", {})
            for currency in currencies:
                if currency in rates and rates[currency] > 0:
                    # API возвращает сколько RUB в 1 USD, нам нужно наоборот, поэтому 1 / rate
                    rate_to_rub = 1 / rates[currency]
                    rates_list.append({"currency": currency, "rate": round(rate_to_rub, 2)})
    except Exception as e:
        logger.error(f"Ошибка при получении курсов валют: {e}")

    # (заглушка) только если список остался пустым
    if not rates_list:
        rates_list = [{"currency": cur, "rate": 75.0} for cur in currencies]
    return rates_list

def get_stock_prices(stocks: List[str]) -> List[Dict[str, float]]:
    stock_list = []
    for stock in stocks:
        try:
            # Yahoo Finance
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
                stock_list.append({"stock": stock, "price": round(price, 2)})
            else:
                stock_list.append({"stock": stock, "price": 100.0}) # Fallback
        except Exception as e:
            logger.error(f"Ошибка при получении цены акции {stock}: {e}")
            stock_list.append({"stock": stock, "price": 100.0}) # Fallback
    return stock_list
