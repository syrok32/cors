import json
import os
import unittest

from src.services import cashback_count
from src.utils import setup_logging

logger = setup_logging("services_log.txt")


class TestCashbackCount(unittest.TestCase):

    def setUp(self) -> None:
        self.data = [
            {"Дата операции": "15.12.2021 12:00:00", "Категория": "Продукты", "Кэшбэк": 100},
            {"Дата операции": "20.12.2021 15:30:00", "Категория": "Рестораны", "Кэшбэк": 50},
            {"Дата операции": "25.11.2021 18:45:00", "Категория": "Продукты", "Кэшбэк": 30},
            {"Дата операции": "01.12.2021 10:15:00", "Категория": "Развлечения", "Кэшбэк": 20},
            {"Дата операции": "15.12.2022 14:20:00", "Категория": "Продукты", "Кэшбэк": 40},
        ]
        self.expected_output = {"Продукты": 100, "Рестораны": 50, "Развлечения": 20}

    def test_cashback_count(self) -> None:
        cashback_count(self.data, 2021, 12)
        with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "json_answer", "cashback_answer.json"),
            "r",
            encoding="utf-8",
        ) as file:
            result = json.load(file)
        self.assertEqual(result, self.expected_output)
