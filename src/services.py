import json
import os
from collections import Counter
from datetime import datetime
from typing import Any

from src.utils import read_in_json, setup_logging

logger = setup_logging("services_log.txt")


def cashback_count(data: Any, year: int, month: int) -> None:
    """Анализирует данные транзакций и вычисляет, сколько кэшбэка можно заработать
    по каждой категории в указанном месяце года."""
    if data is None:
        logger.error("Данные транзакций не были загружены")
        return

    cashback_by_category: Counter = Counter()

    for transaction in data:
        transaction_date = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")
        if transaction_date.year == year and transaction_date.month == month:
            category = transaction["Категория"]
            cashback = transaction["Кэшбэк"] or 0  #
            cashback_by_category[category] += cashback
    try:
        with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "json_answer", "cashback_answer.json"),
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(cashback_by_category, file, ensure_ascii=False, indent=4)
            logger.info("данные записанны")
    except FileNotFoundError:
        logger.error("файд не найден")


cashback_count(read_in_json(), 2021, 12)
