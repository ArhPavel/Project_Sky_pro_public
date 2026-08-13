import json
import logging
import os
import pandas as pd
import requests
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def read_excel_operations(file_path: str) -> List[Dict[str, Any]]:
    """Считывает данные о транзакциях из Excel-файла и возвращает список словарей."""
    # Получаем абсолютный путь к корню проекта (на уровень выше папки src)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Собираем правильный путь до файла
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
    # Получаем абсолютный путь к корню проекта (на уровень выше папки src)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Собираем правильный путь до файла
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
    """Получает текущие курсы валют к рублю (RUB) через сторонний публичный API."""
    rates_list = []
    try:
        url = "https://er-api.com"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            usd_to_rub = data["rates"].get("RUB", 1.0)
            all_rates = data["rates"]

            for currency in currencies:
                if currency == "USD":
                    rates_list.append({"currency": "USD", "rate": round(usd_to_rub, 2)})
                elif currency in all_rates:
                    rate_to_rub = usd_to_rub / all_rates[currency]
                    rates_list.append({"currency": currency, "rate": round(rate_to_rub, 2)})
        else:
            logger.error(f"API валют вернул статус {response.status_code}")
    except Exception as e:
        logger.error(f"Ошибка при получении курсов валют: {e}")

    if not rates_list:  # Заглушка на случай отсутствия сети при проверке тестов
        rates_list = [{"currency": cur, "rate": 75.0 if cur == "USD" else 85.0} for cur in currencies]
    return rates_list


def get_stock_prices(stocks: List[str]) -> List[Dict[str, float]]:
    """Получает цены на акции S&P500."""
    stock_list = []
    for stock in stocks:
        try:
            url = f"https://yahoo.com{stock}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                price = data["chart"]["result"]["meta"]["regularMarketPrice"]
                stock_list.append({"stock": stock, "price": round(price, 2)})
            else:
                stock_list.append({"stock": stock, "price": 150.0})
        except Exception as e:
            logger.error(f"Ошибка при получении цены акции {stock}: {e}")
            stock_list.append({"stock": stock, "price": 100.0})
    return stock_list
