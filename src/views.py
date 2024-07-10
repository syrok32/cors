import json
import os
from typing import Any

from src.utils import (
    api_currency,
    api_stock,
    filter_transactions_date,
    geting_csrds,
    read_in_json,
    read_user_settings_currency,
    read_user_settings_stocks,
    read_xls,
    receive_greeting,
    setup_logging,
    top_5_transactions,
    write_in_json,
)

logger = setup_logging("utils_log.txt")


def main_viewers(time_range: str) -> Any:
    """Главная функция для анализа данных и формирования отчета"""
    data = read_xls("operations.xls")
    write_in_json(data)
    data_json = read_in_json()
    filter_data = filter_transactions_date(data_json, time_range)

    receive_greeting_data = receive_greeting()
    filter_cards = geting_csrds(filter_data)
    top_5_tr = top_5_transactions(filter_data)
    api_currency_data = api_currency(read_user_settings_currency())
    api_stock_data = api_stock(read_user_settings_stocks())

    answer = {
        "greeting": receive_greeting_data,
        "cards": filter_cards,
        "top_transactions": top_5_tr,
        "currency_rates": api_currency_data,
        "stock_prices": api_stock_data,
    }

    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "json_answer", "answer.json"),
        "w",
        encoding="utf-8",
    ) as file:
        try:
            json.dump(answer, file, ensure_ascii=False, indent=4)
            logger.info("Json ответ записан")
        except Exception:
            logger.error("ответ не был записан")


main_viewers("2023-01-01 00:00:00")

# print(api_stock(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]))
