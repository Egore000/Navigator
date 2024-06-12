from app.backend.core.base import BaseDAO
from app.backend.users.models import User


class UsersDAO(BaseDAO):
    model = User
