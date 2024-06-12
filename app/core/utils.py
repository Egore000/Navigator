from datetime import date

from app import exceptions


def validate_date(date_from: date, date_to: date):
    if date_from > date_to:
        raise exceptions.InvalidDateError
