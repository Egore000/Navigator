from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from app.backend import exceptions, responses
from app.backend.core.utils import return_or_raise_error, validate_date, Dates
from app.backend.tasks import tasks

from app.backend.users.auth.dependencies import get_current_user
from app.backend.users.models import User

from app.backend.bookings.schemas import BookingInfo, BookingUpdateScheme
from app.backend.bookings.service import BookingDAO


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@router.get("")
async def get_bookings(
    user: User = Depends(get_current_user)
) -> list[BookingInfo]:
    """Вывод броней текущего пользователя"""
    bookings = await BookingDAO.get_all(user_id=user.id)
    return return_or_raise_error(bookings)


@router.post("")
async def add_booking(
        room_id: int,
        dates: Annotated[Dates, Depends()],
        user: User = Depends(get_current_user)
) -> BookingInfo:
    """Бронирование комнаты в отеле на указанный срок"""
    validate_date(dates.date_from, dates.date_to)

    booking = await BookingDAO.add(user.id, room_id, dates.date_from, dates.date_to)
    if not booking:
        raise exceptions.RoomCannotBeBooked

    booking_dict = parse_obj_as(BookingInfo, booking).dict()
    tasks.send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking


@router.get("/{booking_id}")
async def get_booking(
        booking_id: int,
        user: User = Depends(get_current_user)
) -> BookingInfo:
    """Получение информации о бронировании"""
    booking = await BookingDAO.get_one_or_none(id=booking_id, user_id=user.id)
    return return_or_raise_error(booking)


@router.delete("/{booking_id}")
async def delete_booking(
        booking_id: int,
        user: User = Depends(get_current_user)
):
    """Отмена брони"""
    can_delete = await BookingDAO.check_permissions(user_id=user.id, booking_id=booking_id)
    if can_delete:
        await BookingDAO.delete(item_id=booking_id)
        return responses.DeletedSuccessfullyResponse

    raise exceptions.NotFoundError


@router.patch("/{booking_id}")
async def update_booking(
        booking_id: int,
        booking: Annotated[BookingUpdateScheme, Depends()],
        user: User = Depends(get_current_user),
):
    """Изменение брони"""
    booking = await BookingDAO.update(
        item_id=booking_id,
        user_id=user.id,
        **booking.dict(exclude_unset=True)
    )
    return booking
