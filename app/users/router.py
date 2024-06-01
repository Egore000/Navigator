from typing import Annotated

from fastapi import APIRouter, Depends, Response

from app.config import booking_access_token
from app import exceptions

from app.users.dependencies import get_current_admin_user, get_current_user
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.schemas import UserAuth, UserData
from app.users.models import User
from app.users.service import UsersService


router_auth = APIRouter(
    prefix='/auth',
    tags=['Аутентификация']
)

router_users = APIRouter(
    prefix='/users',
    tags=['Пользователи']
)

@router_auth.post("/register")
async def register_user(user_data: Annotated[UserAuth, Depends()]):
    existing_user: User = await UsersService.get_one_or_none(email=user_data.email)

    if existing_user:
        raise exceptions.UserAlreadyExistsException
    
    hashed_password = get_password_hash(user_data.password)
    await UsersService.add(
        email=user_data.email,
        hashed_password=hashed_password
    )


@router_auth.post("/login")
async def login_user(
    response: Response,
    user_data: Annotated[UserAuth, Depends()]
):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise exceptions.IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(booking_access_token, access_token, httponly=True)
    return {"access_token": access_token}


@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(booking_access_token)


@router_users.get("/me")
async def read_me(current_user: User = Depends(get_current_user)) -> UserData:
    return current_user


@router_users.get("/all")
async def read_all_users(current_user: User = Depends(get_current_admin_user)) -> list[UserData]:
    return await UsersService.get_all()
