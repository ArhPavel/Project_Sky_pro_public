from datetime import datetime
from unittest.mock import patch

from src.views import get_greeting
from src.utils import get_currency_rates, get_stock_prices


# Тест граничных часов (добавляем к существующему test_get_greeting)
def test_get_greeting_boundaries():
    assert get_greeting(datetime(2020, 5, 20, 5, 59, 59)) == "Доброй ночи"
    assert get_greeting(datetime(2020, 5, 20, 6, 0, 0)) == "Доброе утро"
    assert get_greeting(datetime(2020, 5, 20, 23, 0, 0)) == "Доброй ночи"


# Мок для API валют
@patch("src.utils.requests.get")
def test_get_currency_rates_mock(mock_get):
    # Настраиваем фейковый ответ API
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"rates": {"USD": 0.0133, "EUR": 0.011}}  # Примерно 75 и 90 рублей

    rates = get_currency_rates(["USD"])
    assert len(rates) == 1
    assert rates[0]["currency"] == "USD"
    # Проверяем, что запрос не пошел в реальную сеть
    mock_get.assert_called_once()


# Мок для API акций
@patch("src.utils.requests.get")
def test_get_stock_prices_mock(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"chart": {"result": [{"meta": {"regularMarketPrice": 150.5}}]}}

    stocks = get_stock_prices(["AAPL"])
    assert len(stocks) == 1
    assert stocks[0]["stock"] == "AAPL"
    assert stocks[0]["price"] == 150.5

