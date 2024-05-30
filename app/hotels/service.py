from datetime import date

from fastapi import Query

from hotels.rooms.service import RoomsService
from hotels.models import Hotels
from core.base import BaseService

from database import async_session_maker


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


class HotelService(BaseService):
    model = Hotels

    @classmethod
    async def get_all_by_location(
        cls,
        location: str,
        date_from: date,
        date_to: date 
    ):
        async with async_session_maker() as session:
            rooms_left = await RoomsService.get_rooms_left(
                room_id=2,
                date_from=date_from,
                date_to=date_to
            )
            print(rooms_left)