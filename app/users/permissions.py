from enum import Enum

from fastapi import Depends

from app import exceptions
from app.users.auth.dependencies import get_current_user
from app.users.models import User


class UserRole(str, Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role is UserRole.admin.value:
        raise exceptions.AccessForbiddenException
    return current_user


async def get_current_moderator_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role not in (UserRole.admin.value,
                                 UserRole.moderator.value):
        raise exceptions.AccessForbiddenException
    return current_user
