from sqlalchemy import select

from core.base import BaseService
from bookings.models import Bookings
from database import async_session_maker



class BookingService(BaseService):
    model = Bookings