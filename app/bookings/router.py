from datetime import date
from fastapi import APIRouter, Depends

from app.exceptions import RoomCannotBeBooked

from app.users.auth.dependencies import get_current_user
from app.users.models import User

from app.bookings.schemas import BookingScheme
from app.bookings.service import BookingService

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@router.get("")
async def get_bookings(user: User = Depends(get_current_user)) -> list[BookingScheme]:
    return await BookingService.get_all(user_id=user.id)


@router.post("")
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    user: User = Depends(get_current_user)
):
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked


@router.delete("/{booking_id}")
async def delete_booking(
    booking_id: int,
    user: User = Depends(get_current_user)
):
    await BookingService.delete(item_id=booking_id)
