from app.core.base import BaseService
from app.users.models import User


class UsersService(BaseService):
    model = User
