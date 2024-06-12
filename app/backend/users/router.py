from fastapi import APIRouter, Depends

from app.backend.core.utils import return_or_raise_error
from app.backend.users.auth.dependencies import get_current_user
from app.backend.users.permissions import get_current_admin_user
from app.backend.users.schemas import UserData
from app.backend.users.models import User
from app.backend.users.service import UsersDAO


router = APIRouter(
    prefix='/users',
    tags=['Пользователи']
)


@router.get("/me")
async def read_me(
        current_user: User = Depends(get_current_user)
) -> UserData:
    """Мой профиль"""
    return current_user


@router.get("/all")
async def read_all_users(
        current_user: User = Depends(get_current_admin_user)
) -> list[UserData]:
    """Получить всех пользователей сайта"""
    users = await UsersDAO.get_all()
    return return_or_raise_error(users)
