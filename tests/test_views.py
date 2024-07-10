import unittest
from unittest.mock import MagicMock, mock_open, patch
from typing import Any
from src.views import main_viewers


class TestMainViewers(unittest.TestCase):

    @patch("src.views.read_xls", return_value=[{"Сумма операции": 100}, {"Сумма операции": -50}])
    @patch("src.views.write_in_json")
    @patch("src.views.read_in_json", return_value=[{"Сумма операции": 100}, {"Сумма операции": -50}])
    @patch("src.views.filter_transactions_date", return_value=[{"Сумма операции": 100}])
    @patch("src.views.receive_greeting", return_value="Доброе утро")
    @patch("src.views.geting_csrds", return_value=[{"last_digits": "1234", "total_spent": 100, "cashback": 1}])
    @patch("src.views.top_5_transactions", return_value=[{"Сумма операции": 100}])
    @patch("src.views.api_currency", return_value=[{"currency": "USD", "rate": 75.0}])
    @patch("src.views.api_stock", return_value=[{"stock": "AAPL", "price": 150.0}])
    @patch("src.views.read_user_settings_currency", return_value=["USD"])
    @patch("src.views.read_user_settings_stocks", return_value=["AAPL"])
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("src.views.setup_logging")  # Mock setup_logging to avoid actual logging
    def test_main_viewers(
        self,

        mock_setup_logging: Any,
        mock_json_dump: Any,
        mock_open_func: Any,
        mock_read_user_settings_stocks: Any,
        mock_read_user_settings_currency: Any,
        mock_api_stock: Any,
        mock_api_currency: Any,
        mock_top_5: Any,
        mock_geting_csrds: Any,
        mock_receive_greeting: Any,
        mock_filter_transactions_date: Any,
        mock_read_in_json: Any,
        mock_write_in_json: Any,
        mock_read_xls: Any,
    ) -> None:

        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger

        time_range = "2023-01-01 00:00:00"
        main_viewers(time_range)

        mock_json_dump.assert_called_once()

        args, _ = mock_json_dump.call_args
        written_data = args[0]

        expected_answer = {
            "greeting": "Доброе утро",
            "cards": [{"last_digits": "1234", "total_spent": 100, "cashback": 1}],
            "top_transactions": [{"Сумма операции": 100}],
            "currency_rates": [{"currency": "USD", "rate": 75.0}],
            "stock_prices": [{"stock": "AAPL", "price": 150.0}],
        }

        self.assertEqual(written_data, expected_answer)


if __name__ == "__main__":
    unittest.main()
