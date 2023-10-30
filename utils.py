from exceptions import (
    NegativeTitlesError,
    InvalidYearCupError,
    ImpossibleTitlesError,
)  # noqa
from datetime import date, datetime


def data_processing(data: dict):
    if data["titles"] < 0:
        raise NegativeTitlesError()

    first_cup = datetime.strptime(data["first_cup"], "%Y-%m-%d")
    count_year = first_cup.year - 1930

    if first_cup.year < 1930 or count_year % 4 != 0:
        raise InvalidYearCupError()

    today = date.today().year
    confer_tiyle_year = today - first_cup.year

    if confer_tiyle_year / 4 < data["titles"]:
        raise ImpossibleTitlesError()
