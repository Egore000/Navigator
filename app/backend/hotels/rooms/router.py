from typing import Annotated

from fastapi import APIRouter, Depends

from fastapi_cache.decorator import cache

from app.backend.core.utils import validate_date, return_or_raise_error, Dates
from app.backend.hotels.rooms.schemas import RoomScheme, RoomInfo
from app.backend.hotels.rooms.service import RoomsDAO
from app.backend.users.auth.dependencies import get_current_user
from app.backend.users.models import User


router = APIRouter(
    prefix="/hotel/{hotel_id}/rooms",
    tags=["Комнаты"]
)


@router.get("")
@cache(expire=60)
async def get_rooms_by_time(
        hotel_id: int,
        dates: Annotated[Dates, Depends()],
) -> list[RoomInfo]:
    """Поиск комнат в отеле на указанный срок"""
    validate_date(dates.date_from, dates.date_to)
    rooms = await RoomsDAO.search_for_rooms(hotel_id, dates.date_from, dates.date_to)
    return return_or_raise_error(rooms)


@router.get("/all")
async def get_all_rooms(
        hotel_id: int,
        user: User = Depends(get_current_user)
) -> list[RoomScheme]:
    """Вывод всех комнат в отеле"""
    rooms = await RoomsDAO.get_all(hotel_id)
    return return_or_raise_error(rooms)
