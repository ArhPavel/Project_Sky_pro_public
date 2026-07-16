from unittest.mock import Mock, patch

from src.external_api import convert_to_rubles


@patch("src.external_api.get_exchange_rate", return_value=90.0)
def test_convert_usd_to_rub(mock_get_rate: Mock) -> None:
    transaction = {"amount": 100, "currency": "USD"}
    result = convert_to_rubles(transaction)

    assert result == 9000.0  # 100 * 90
    mock_get_rate.assert_called_once_with("USD", "RUB")


@patch("src.external_api.get_exchange_rate", return_value=100.5)
def test_convert_eur_to_rub(mock_get_rate: Mock) -> None:
    transaction = {"amount": 50, "currency": "EUR"}
    result = convert_to_rubles(transaction)

    assert result == 5025.0  # 50 * 100.5
    mock_get_rate.assert_called_once_with("EUR", "RUB")


def test_convert_rub_no_api_call() -> None:
    with patch("src.external_api.get_exchange_rate") as mock_rate:
        transaction = {"amount": 1234.5, "currency": "RUB"}
        result = convert_to_rubles(transaction)
        assert result == 1234.5
        mock_rate.assert_not_called()


@patch("src.external_api.get_exchange_rate")
def test_convert_unknown_currency_returns_zero(mock_get_rate: Mock) -> None:
    transaction = {"amount": 100, "currency": "JPY"}
    result = convert_to_rubles(transaction)
    assert result == 0.0
    mock_get_rate.assert_not_called()
