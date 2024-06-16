from datetime import date

from sqlalchemy import insert, select, func, and_, update

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
                price = await RoomsDAO.get_room_price(room_id)

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
    async def update(cls, item_id: int, **values):
        data = values.copy()

        room_id = data.pop("room_id")
        if room_id is not None:
            price = await RoomsDAO.get_room_price(room_id)

            data.update({
                "price": price,
                "room_id": room_id,
            })

        booking = await super().update(item_id, **data)
        return booking.scalar()

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
                cls.model
            ).values(
                room_id=room_id,
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
                price=price
            ).returning(
                cls.model
            )

    @classmethod
    async def check_permissions(cls, user_id: int, booking_id: int) -> bool:
        """Проверка принадлежности брони пользователю"""

        is_booking_in_user_bookings = select(
            func.count(cls.model.id)
        ).select_from(
            cls.model
        ).where(
            and_(
                cls.model.user_id == user_id,
                cls.model.id == booking_id,
            )
        )
        async with async_session_maker() as session:
            permission = await session.execute(is_booking_in_user_bookings)
            return bool(permission.scalar())
