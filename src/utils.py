import json
import logging
import os
from datetime import datetime
from logging import Logger
from typing import Any, Dict, List

import numpy as np
import pandas
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("Token")
headers = {"apikey": f"{TOKEN}"}

TOKEN_02 = os.getenv("Token_02")
headers_02 = {"apikey": f"{TOKEN_02}"}


def setup_logging(name_file: str) -> Logger:
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler(name_file, encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger


logger = setup_logging("utils_log.txt")


def read_xls(file_name: Any) -> Any:
    """Получаеи словарь из xls фйла"""
    try:
        df_transactions = pd.read_excel(f"../data/{file_name}")
        df_transactions = df_transactions.replace({np.nan: None})
        logger.info("файл прчитан operations.xls ")
        return df_transactions.to_dict(
            orient="records",
        )
    except FileNotFoundError:
        logger.error("неправельный файд")


def write_in_json(dict_pd: List[Dict[str, Any]]) -> None:
    """Записывает данные в JSON файл"""

    try:
        with open("info.json", "w", encoding="utf-8") as file:
            json.dump(dict_pd, file, ensure_ascii=False, indent=4)
            logger.info("данные записанны в файл")
    except FileNotFoundError:
        logger.error("ошибка записи в файл")


def read_in_json() -> Any:
    """Читает данные из JSON файла"""
    try:
        with open("info.json", encoding="utf-8") as file:
            data_dict = json.load(file)
            logger.info("json файл прочитан")
            return data_dict
    except FileNotFoundError:
        logger.error("файл не найден")


def read_user_settings_currency() -> Any:
    """Читает настройки пользователя для валют"""
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "user_settings.json"), "r", encoding="utf-8"
    ) as file:
        dict_currency = json.load(file)
        logger.info("Данные получены (валюты)")
        return dict_currency["user_currencies"]


def read_user_settings_stocks() -> Any:
    """Читает настройки пользователя для акций"""
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "user_settings.json"), "r", encoding="utf-8"
    ) as file:
        dict_currency = json.load(file)
        logger.info("Данные получены (акции)")
        return dict_currency["user_stocks"]


def filter_transactions_date(transactions: List[Dict[str, Any]], date_str: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по указанной дате в виде диопазона"""
    end_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    start_date = datetime(end_date.year, end_date.month, 1)

    try:
        filtered_transactions = [
            transaction
            for transaction in transactions
            if start_date <= datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S") <= end_date
        ]
        sorted_list = sorted(
            filtered_transactions,
            key=lambda x: datetime.strptime(x["Дата операции"], "%d.%m.%Y %H:%M:%S"),
            reverse=False,
        )
        logger.info("фильтрация прошла")
        return sorted_list
    except Exception:
        logger.error("ошибка")
        return []


def receive_greeting() -> str:
    """Возвращает приветствие в зависимости от текущего времени"""
    current_data = datetime.now()
    current_data_hour = current_data.hour
    if 6 <= current_data_hour < 12:
        return "Доброе утро"
    elif 12 <= current_data_hour < 18:
        return "Добрый день"
    elif 18 <= current_data_hour < 23:
        return "Добрый вечер"
    elif 0 <= current_data_hour < 6:
        return "Доброй ночи"
    else:
        return "Добро пожаловать"


def info_cards(data_transactions: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """Возвращает информацию о картах и их транзакциях"""
    card_summary = {}

    for transaction in data_transactions:
        card_number = transaction.get("Номер карты")
        if card_number is None:
            continue

        last_4_digits = card_number[-4:]
        amount = transaction.get("Сумма операции", 0)

        if last_4_digits not in card_summary:
            card_summary[last_4_digits] = {"total_expenses": 0, "total_cashback": 0}

        card_summary[last_4_digits]["total_expenses"] += round(abs(amount))
        card_summary[last_4_digits]["total_cashback"] += int(abs(amount) // 100)

    return card_summary


def geting_csrds(transactions: Any) -> Any:
    """Возвращает список с информацией о картах, тратах, кешбеках"""

    new_list = []
    card_summary = info_cards(transactions)
    for card, summary in card_summary.items():
        new_list.append(
            {"last_digits": card, "total_spent": summary["total_expenses"], "cashback": summary["total_cashback"]}
        )
    logger.info("Данные карты выведенны")
    return new_list


def top_5_transactions(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Функция возвращает список из пяти самых дорогих транзакций."""

    sort_data = sorted(data, key=lambda x: x["Сумма операции"], reverse=True)
    logger.info("топ 5 операций работают")
    return sort_data[:5]


def api_currency(currency: List[str]) -> List[Dict[str, Any]]:
    """Возвращает текущий курс валют"""
    new_list = []
    for i in currency:
        url = f"https://api.apilayer.com/fixer/latest?symbols=RUB&base={i}"

        try:
            response = requests.request(
                "GET",
                url,
                headers=headers,
            )
            result = response.json()
            new_list.append({"currency": f"{i}", "rate": result["rates"]["RUB"]})
        except Exception:
            new_list.append({"currency": f"{i}", "rate": "не удолось получить валюту"})

    logger.info("api валюты получен")
    return new_list


def api_stock(stocks: Any) -> Any:
    """Возвращает текущую цену акций"""
    new_list_stock = list()
    for i in stocks:
        url_st = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={i}&apikey={TOKEN_02}"
        response = requests.request(
            "GET",
            url_st,
            headers=headers_02,
        )
        data = response.json()
        try:
            new_list_stock.append({"stock": f"{i}", "price": data["Global Quote"]["05. price"]})

        except KeyError:
            new_list_stock.append({"stock": f"{i}", "price": "error"})
    logger.info("api акций получен")
    return new_list_stock
