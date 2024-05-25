from datetime import date
from typing import Optional

from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
import uvicorn 


app = FastAPI()


class Hotel(BaseModel):
    address: str
    name: str
    stars: int = Query(None, ge=1, le=5)


class HotelsSearchArgs:
    def __init__(
        self,
        location: str,
        date_from: date,
        date_to: date,
        has_spa: bool = None,
        stars: int = Query(None, ge=1, le=5),
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars



@app.get("/hotels")
def get_hotels(
    search_args: HotelsSearchArgs = Depends()
) -> list[Hotel]:
    hotels = [
        {
            "address": "пер.Буяновский, д.3А",
            "name": "Парус",
            "stars": 4
        },
        {
            "address": "ул.Пушкина, д.Колотушкина",
            "name": "Плаза-Хотел",
            "stars": 3
        },
        {
            "address": "ул.Гагарина, д.3",
            "name": "Космос",
            "stars": 5
        }
    ]
    return hotels


class Booking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post("/bookings")
def add_booking(booking: Booking):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)