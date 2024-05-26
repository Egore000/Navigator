from fastapi import APIRouter
from sqlalchemy import select

from bookings.schemas import Booking
from bookings.service import BookingService
from bookings.models import Bookings
from database import async_session_maker


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@router.get("")
async def get_bookings() -> list[Booking]:
    return await BookingService.get_all()


@router.post("")
async def add_booking(booking: Booking):
    pass

