import os
import unittest
from typing import Any
import pandas as pd

from src.reports import spending_by_category


class TestSpendingByCategory(unittest.TestCase):

    def setUp(self) -> None:
        # Фиктивные данные транзакций
        self.data = {
            "Дата операции": [
                "01.09.2021 12:00:00",
                "15.10.2021 12:00:00",
                "25.11.2021 12:00:00",
                "05.12.2021 12:00:00",
            ],
            "Категория": ["Пополнения", "Пополнения", "Продукты", "Пополнения"],
            "Сумма платежа": [100, 400, 200, 250],
        }
        self.df = pd.DataFrame(self.data)

    def test_spending_by_category(self) -> None:
        result = spending_by_category(self.df, "Пополнения", "01-12-2021")
        expected_result = {"Категория": "Пополнения", "сумма": 400}  # Исправление суммы
        self.assertEqual(result, expected_result)

    def test_file_existence(self) -> Any:
        # Построение пути
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_directory = os.path.join(base_dir, "..", "data")
        file_name = "operations.xls"
        file_path = os.path.join(data_directory, file_name)

        # Проверка наличия файла
        assert os.path.exists(file_path), f"Нет такого файла или директории: '{file_path}'"
