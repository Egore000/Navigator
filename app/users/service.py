from core.base import BaseService
from users.models import User


class UsersService(BaseService):
    model = User