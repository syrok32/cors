import json
import os
from datetime import datetime, timedelta
from typing import Any, Callable, Optional

import pandas as pd

from src.utils import setup_logging


def read_df() -> Any:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", "data", "operations.xls")

    # Проверка наличия файла перед чтением
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Нет такого файла или директории: '{file_path}'")

    datef = pd.read_excel(file_path)
    return datef


logger = setup_logging("reports_log.txt")


def save_report_to_file(filename: Optional[str] = None) -> Callable:
    """Декоратор для сохранения результата функции в файл JSON."""

    def decorator(func: Any) -> Any:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            output_filename = filename if filename else "report.json"
            with open(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "json_answer", output_filename),
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
                logger.info("данные записанны в файл")
            return result

        return wrapper

    return decorator


@save_report_to_file("answewr_category.json")
def spending_by_category(df: pd.DataFrame, category: Any, date: Any = None) -> Any:
    """Рассчитывает траты по заданной категории за последние три месяца от переданной даты."""
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%d-%m-%Y")

    date_end = date - timedelta(days=90)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    date_filter = df[(df["Категория"] == category) & (df["Дата операции"] >= date_end) & (df["Дата операции"] <= date)]
    total_coast = date_filter["Сумма платежа"].sum()
    logger.info("успешно")
    return {"Категория": category, "сумма": float(total_coast)}


print(spending_by_category(read_df(), "Пополнения", "1-12-2021"))
