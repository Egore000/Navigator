from datetime import date, datetime, timedelta
from fastapi import APIRouter, Query, Depends

from app.backend import exceptions
from app.backend.core.utils import validate_date
from app.backend.hotels.rooms.schemas import RoomScheme, RoomInfo
from app.backend.hotels.rooms.service import RoomsDAO
from app.backend.users.permissions import (
    get_current_admin_user

)
from app.backend.users.models import User


router = APIRouter(
    prefix="/hotel/{hotel_id}/rooms",
    tags=["Комнаты"]
)


@router.get("")
async def get_rooms_by_time(
    hotel_id: int,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например, {datetime.now().date() + timedelta(days=1)}")
) -> list[RoomInfo]:
    """Поиск комнат в отеле по заданным срокам"""
    validate_date(date_from, date_to)

    rooms = await RoomsDAO.search_for_rooms(hotel_id, date_from, date_to)

    if not rooms:
        raise exceptions.NotFoundError
    return rooms


@router.get("/all")
async def get_all_rooms(
    hotel_id: int,
    user: User = Depends(get_current_admin_user)
) -> list[RoomScheme]:
    """Вывод всех комнат в отеле (для админа)"""
    return await RoomsDAO.get_all(hotel_id)
