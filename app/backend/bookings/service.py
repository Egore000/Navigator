from datetime import date

from sqlalchemy import insert

from app.backend.core.base import BaseDAO
from app.backend.bookings.models import Bookings
from app.backend.hotels.rooms.service import RoomsDAO

from app.backend.database import async_session_maker


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        """Бронирование комнаты пользователем на некоторый период времени"""
        async with async_session_maker() as session:
            rooms_left = await RoomsDAO.get_rooms_left_count(
                room_id=room_id,
                date_from=date_from,
                date_to=date_to
            )

            if rooms_left > 0:
                get_price = await RoomsDAO.get_room_price(room_id)
                price = await session.execute(get_price)
                price = price.scalar()

                new_booking_query = await cls._add_booking(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                )
                new_booking = await session.execute(new_booking_query)
                await session.commit()
                return new_booking.scalar()
            else:
                return None
            
    @classmethod
    async def _add_booking(
        cls,
        room_id: int,
        user_id: int,
        date_from: date,
        date_to: date,
        price: int
    ):
        return insert(
                Bookings
            ).values(
                room_id=room_id,
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
                price=price
            ).returning(
                Bookings
            )
