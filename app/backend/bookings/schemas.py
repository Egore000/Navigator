from datetime import date

from fastapi import Query
from pydantic import BaseModel

from app.backend.core.utils import today, tomorrow


class BookingInfo(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date 
    date_to: date
    price: int
    total_cost: int
    total_days: int

    class Config:
        orm_mode = True


class BookingUpdateScheme(BaseModel):
    room_id: int | None
    date_from: date = Query(
        None,
        description=f"Например, {today}"
    )
    date_to: date = Query(
        None,
        description=f"Например, {tomorrow}"
    )