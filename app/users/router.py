from fastapi import APIRouter, Depends

from app.users.auth.dependencies import get_current_user
from app.users.permissions import get_current_admin_user
from app.users.schemas import UserData
from app.users.models import User
from app.users.service import UsersService


router = APIRouter(
    prefix='/users',
    tags=['Пользователи']
)


@router.get("/me")
async def read_me(current_user: User = Depends(get_current_user)) -> UserData:
    return current_user


@router.get("/all")
async def read_all_users(current_user: User = Depends(get_current_admin_user)) -> list[UserData]:
    return await UsersService.get_all()
