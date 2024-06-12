from datetime import date
from fastapi import APIRouter, Depends, Query

from app.backend import exceptions, responses
from app.backend.core.utils import return_or_raise_error, validate_date, \
    tomorrow, today

from app.backend.users.auth.dependencies import get_current_user
from app.backend.users.models import User

from app.backend.bookings.schemas import BookingScheme
from app.backend.bookings.service import BookingDAO


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@router.get("")
async def get_bookings(
    user: User = Depends(get_current_user)
) -> list[BookingScheme]:
    """Вывод броней текущего пользователя"""
    bookings = await BookingDAO.get_all(user_id=user.id)
    return return_or_raise_error(bookings)


@router.post("")
async def add_booking(
        room_id: int,
        date_from: date = Query(
            ...,
            description=f"Например, {today}"
        ),
        date_to: date = Query(
            ...,
            description=f"Например, {tomorrow}"
        ),
        user: User = Depends(get_current_user)
) -> responses.JSONResponse:
    """Бронирование комнаты в отеле на указанный срок"""
    validate_date(date_from, date_to)
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise exceptions.RoomCannotBeBooked
    return responses.CreatedSuccessfullyResponse


@router.delete("/{booking_id}")
async def delete_booking(
        booking_id: int,
        user: User = Depends(get_current_user)
) -> responses.JSONResponse:
    """Отмена брони"""
    await BookingDAO.delete(item_id=booking_id)
    return responses.DeletedSuccessfullyResponse
