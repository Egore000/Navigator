from datetime import date, datetime, timedelta
from typing import Any

from fastapi import Query

from app.backend import exceptions


def validate_date(date_from: date, date_to: date):
    if date_from > date_to:
        raise exceptions.InvalidDateError


def return_or_raise_error(some: Any) -> Any:
    if not some:
        raise exceptions.NotFoundError
    return some


today = datetime.now().date()
tomorrow = today + timedelta(days=1)
