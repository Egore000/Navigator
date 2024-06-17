from sqladmin import ModelView

from app.backend.bookings.models import Bookings
from app.backend.hotels.models import Hotels
from app.backend.hotels.rooms.models import Rooms
from app.backend.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.role]
    column_details_exclude_list = [
        User.hashed_password,
    ]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.room]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel, Rooms.booking]
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user, Bookings.room]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"
