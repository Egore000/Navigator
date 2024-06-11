from datetime import date, datetime, timedelta
from fastapi import APIRouter, Query, Depends

from app import exceptions
from app.core.utils import validate_date
from app.hotels.rooms.schemas import RoomScheme, RoomInfo
from app.hotels.rooms.service import RoomsDAO
from app.users.auth.dependencies import get_current_user
from app.users.permissions import UserRole
from app.users.models import User


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
    user: User = Depends(get_current_user)
) -> list[RoomScheme]:
    """Вывод всех комнат в отеле"""
    if user.role == UserRole.admin.value:
        return await RoomsDAO.get_all(hotel_id)
    raise exceptions.AccessForbiddenException
