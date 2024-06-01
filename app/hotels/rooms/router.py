from datetime import date, datetime, timedelta
from fastapi import APIRouter, Query, Depends

from app import exceptions
from app.hotels.rooms.schemas import RoomScheme, RoomInfo
from app.hotels.rooms.service import RoomsService
from app.users.dependencies import get_current_user, UserRole
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
    return await RoomsService.search_for_room(hotel_id, date_from, date_to)


@router.get("/all")
async def get_all_rooms(
    hotel_id: int,
    user: User = Depends(get_current_user)
) -> list[RoomScheme]:
    if user.role == UserRole.admin.value:
        return await RoomsService.get_all(hotel_id)
    raise exceptions.AccessForbiddenException
