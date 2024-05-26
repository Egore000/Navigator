from fastapi import APIRouter, Depends, Request
from sqlalchemy import select

from users.dependencies import get_current_user
from users.models import Users

from bookings.schemas import Booking
from bookings.service import BookingService
from bookings.models import Bookings
from database import async_session_maker


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) : # -> list[Booking]:
    return await BookingService.get_all(user_id=user.id)


@router.post("")
async def add_booking(booking: Booking):
    pass

