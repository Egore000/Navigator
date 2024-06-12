from fastapi import APIRouter, Depends

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
    return current_user


@router.get("/all")
async def read_all_users(
    current_user: User = Depends(get_current_admin_user)
) -> list[UserData]:
    return await UsersDAO.get_all()
