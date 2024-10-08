from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_versioning import version
from pydantic import parse_obj_as

from app.backend import exceptions, responses
from app.backend.bookings.schemas import BookingInfo
from app.backend.bookings.service import BookingDAO
from app.backend.core.utils import Dates, return_or_raise_error, today, tomorrow, validate_date
from app.backend.tasks import tasks
from app.backend.users.auth.dependencies import get_current_user
from app.backend.users.models import User

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@router.get("")
@version(1)
async def get_bookings(
    user: User = Depends(get_current_user)
) -> list[BookingInfo]:
    """Вывод броней текущего пользователя"""
    bookings = await BookingDAO.get_all(user_id=user.id)
    return return_or_raise_error(bookings)


@router.post("", response_model=BookingInfo)
@version(1)
async def add_booking(
        room_id: int,
        dates: Annotated[Dates, Depends()],
        user: User = Depends(get_current_user)
):
    """Бронирование комнаты в отеле на указанный срок"""
    validate_date(dates.date_from, dates.date_to)

    booking = await BookingDAO.insert(user.id, room_id, dates.date_from, dates.date_to)
    if not booking:
        raise exceptions.RoomCannotBeBooked

    booking_dict = parse_obj_as(BookingInfo, booking).dict()
    tasks.send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking


@router.get("/{booking_id}")
@version(1)
async def get_booking(
        booking_id: int,
        user: User = Depends(get_current_user)
) -> BookingInfo:
    """Получение информации о бронировании"""
    booking = await BookingDAO.get_one_or_none(id=booking_id, user_id=user.id)
    return return_or_raise_error(booking)


@router.delete("/{booking_id}")
@version(1)
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
@version(1)
async def update_booking(
        booking_id: int,
        room_id: int | None = None,
        date_from: Annotated[
            date | None,
            Query(description=f"Например, {today}")
        ] = None,
        date_to: Annotated[
            date | None,
            Query(description=f"Например, {tomorrow}")
        ] = None,
        user: User = Depends(get_current_user),
) -> BookingInfo:
    """Изменение брони"""
    is_owner = await BookingDAO.check_permissions(user.id, booking_id)
    if not is_owner:
        raise exceptions.AccessForbiddenException

    booking = await BookingDAO.get_one_or_none(id=booking_id)

    if date_from is None:
        date_from = booking.get("date_from")

    if date_to is None:
        date_to = booking.get("date_to")

    validate_date(date_from, date_to)

    booking = await BookingDAO.update(
        item_id=booking_id,
        room_id=room_id,
        user_id=user.id,
        date_from=date_from,
        date_to=date_to,
    )
    return booking
