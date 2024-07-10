import json
import logging
from typing import Any
from unittest.mock import Mock, mock_open, patch

import pandas as pd
import pytest

from src.utils import (filter_transactions_date, geting_csrds, info_cards, read_in_json, read_user_settings_currency,
                       read_user_settings_stocks, read_xls, setup_logging, top_5_transactions, write_in_json)

sample_transactions = [
    {
        "Дата операции": "31.12.2021 16:44:00",
        "Дата платежа": "31.12.2021",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -160.89,
        "Валюта операции": "RUB",
        "Сумма платежа": -160.89,
        "Валюта платежа": "RUB",
        "Кэшбэк": None,
        "Категория": "Супермаркеты",
        "MCC": 5411.0,
        "Описание": "Колхоз",
        "Бонусы (включая кэшбэк)": 3,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 160.89,
    },
    {
        "Дата операции": "31.12.2021 16:42:04",
        "Дата платежа": "31.12.2021",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -64.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -64.0,
        "Валюта платежа": "RUB",
        "Кэшбэк": None,
        "Категория": "Супермаркеты",
        "MCC": 5411.0,
        "Описание": "Колхоз",
        "Бонусы (включая кэшбэк)": 1,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 64.0,
    },
    {
        "Дата операции": "31.12.2021 16:39:04",
        "Дата платежа": "31.12.2021",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -118.12,
        "Валюта операции": "RUB",
        "Сумма платежа": -118.12,
        "Валюта платежа": "RUB",
        "Кэшбэк": None,
        "Категория": "Супермаркеты",
        "MCC": 5411.0,
        "Описание": "Магнит",
        "Бонусы (включая кэшбэк)": 2,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 118.12,
    },
]

sample_currency_response = {"rates": {"RUB": 75.0}}

sample_stock_response = {"Global Quote": {"01. symbol": "IBM", "05. price": "135.67"}}


@pytest.fixture
def setup_logging_fixture() -> Any:
    logger = setup_logging("test_log.txt")
    return logger


def test_setup_logging(setup_logging_fixture: Any) -> None:
    logger = setup_logging_fixture
    assert logger is not None
    assert logger.level == logging.INFO


def test_read_xls(monkeypatch: Any) -> None:
    mock_df = pd.DataFrame(sample_transactions)
    monkeypatch.setattr(pd, "read_excel", lambda x: mock_df)
    result = read_xls("test.xls")
    assert isinstance(result, list)
    assert len(result) == 3


def test_write_in_json(monkeypatch: Any) -> None:
    mock_open_func = mock_open()
    with patch("builtins.open", mock_open_func):
        write_in_json(sample_transactions)
    mock_open_func.assert_called_once_with("info.json", "w", encoding="utf-8")


def test_read_in_json(monkeypatch: Any) -> None:
    mock_open_func = mock_open(read_data=json.dumps(sample_transactions))
    with patch("builtins.open", mock_open_func):
        result = read_in_json()
    assert isinstance(result, list)
    assert len(result) == 3


def test_read_user_settings_currency(monkeypatch: Any) -> None:
    mock_open_func = mock_open(
        read_data=json.dumps({"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]})
    )
    with patch("builtins.open", mock_open_func):
        result = read_user_settings_currency()
    assert isinstance(result, list)
    assert result == ["USD", "EUR"]


def test_read_user_settings_stocks(monkeypatch: Any) -> None:
    mock_open_func = mock_open(
        read_data=json.dumps({"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]})
    )
    with patch("builtins.open", mock_open_func):
        result = read_user_settings_stocks()
    assert isinstance(result, list)
    assert result == ["AAPL", "GOOGL"]


def test_filter_transactions_date() -> None:
    result = filter_transactions_date(sample_transactions, "2023-07-10 23:59:59")
    assert isinstance(result, list)
    assert len(result) == 0


def test_receive_greeting_morning() -> None:
    mock_receive_greeting = Mock(return_value="Доброе утро")
    assert mock_receive_greeting() == "Доброе утро"


def test_info_cards() -> None:
    result = info_cards(sample_transactions)
    assert isinstance(result, dict)
    assert len(result) == 1


def test_geting_csrds() -> None:
    result = geting_csrds(sample_transactions)
    assert isinstance(result, list)
    assert len(result) == 1


def test_top_5_transactions() -> None:

    result = top_5_transactions(sample_transactions)
    assert isinstance(result, list)
    assert len(result) == 3


# @patch("requests.request")
# def test_api_currency(mock_request: Any) ->None:
#     mock_request.return_value.json.return_value = sample_currency_response
#     result = api_currency(["USD"])
#     assert isinstance(result, list)
#     assert len(result) == 1
#     assert result[0]["rate"] == 75.0
