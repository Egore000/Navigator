from datetime import date

from sqlalchemy import insert, select, func, and_, ScalarResult

from app.backend.core.base import BaseDAO
from app.backend.bookings.models import Bookings
from app.backend.core.utils import validate_date
from app.backend.hotels.rooms.service import RoomsDAO

from app.backend.database import async_session_maker


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def insert(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ) -> ScalarResult[Bookings] | None:
        """Бронирование комнаты пользователем на некоторый период времени"""
        rooms_left = await RoomsDAO.get_rooms_left_count(room_id, date_from, date_to)

        if rooms_left > 0:
            price = await RoomsDAO.get_room_price(room_id)

            new_booking = await super().insert(
                room_id=room_id,
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
                price=price
            )
            return new_booking.scalar()

        return None

    @classmethod
    async def update(cls, item_id: int, **values) -> ScalarResult[Bookings]:
        """Обновление информации о брони"""
        if "room_id" in values:
            room_id = values.get("room_id")
            if room_id is None:
                values.pop("room_id")
            else:
                price = await RoomsDAO.get_room_price(room_id)
                values.update({"price": price})

        booking = await super().update(item_id, **values)
        return booking

    @classmethod
    async def check_permissions(cls, user_id: int, booking_id: int) -> bool:
        """Проверка принадлежности брони пользователю"""
        query = (
            select(func.count(cls.model.id))
            .filter_by(id=booking_id, user_id=user_id)
        )
        permission = await cls.execute(query)
        return bool(permission.scalar())
