from fastapi import Query
from pydantic import BaseModel


class HotelScheme(BaseModel):
    address: str
    name: str
    stars: int = Query(None, ge=1, le=5)

    class Config:
        orm_mode = True
