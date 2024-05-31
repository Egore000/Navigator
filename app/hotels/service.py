from datetime import date

from app.database import async_session_maker

from app.hotels.rooms.service import RoomsService
from app.hotels.models import Hotels
from app.core.base import BaseService


class HotelService(BaseService):
    model = Hotels

    @classmethod
    async def search_for_hotels(
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
