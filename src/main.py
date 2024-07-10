import pandas as pd

from src.reports import read_df, spending_by_category
from src.services import cashback_count
from src.utils import read_in_json
from src.views import main_viewers

datef = pd.read_excel("../data//operations.xls")


def main() -> None:
    """вызов всех функций"""
    spending_by_category(read_df(), "Пополнения", "1-12-2021")
    cashback_count(read_in_json(), 2021, 12)
    main_viewers("2021-12-31 15:44:39")


if __name__ == "__main__":
    main()
