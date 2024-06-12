from fastapi import Query
from pydantic import BaseModel


class HotelScheme(BaseModel):
    id: int
    location: str
    name: str
    stars: int = Query(None, ge=1, le=5)

    class Config:
        orm_mode = True


class HotelInfo(HotelScheme):
    services: list[str | None]
    rooms_quantity: int
    image_id: int
    rooms_left: int | None = None
