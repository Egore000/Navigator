from typing import Annotated

from fastapi import APIRouter, Depends, Response

from app.config import booking_access_token, booking_refresh_token
from app import exceptions

from app.users.auth.dependencies import get_current_user_for_refresh
from app.users.auth.auth import authenticate_user, get_password_hash, JWTToken
from app.users.auth.schemas import UserAuth, TokenInfo
from app.users.models import User
from app.users.service import UsersService


router = APIRouter(
    prefix='/auth',
    tags=['Аутентификация']
)


@router.post("/register")
async def register_user(user_data: Annotated[UserAuth, Depends()]):
    existing_user: User = await UsersService.get_one_or_none(email=user_data.email)

    if existing_user:
        raise exceptions.UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    await UsersService.add(
        email=user_data.email,
        hashed_password=hashed_password
    )


@router.post("/login")
async def login_user(
        response: Response,
        user_data: Annotated[UserAuth, Depends()]
) -> TokenInfo:
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise exceptions.IncorrectEmailOrPasswordException

    access_token = JWTToken.create("access", {"sub": str(user.id)})
    refresh_token = JWTToken.create("refresh", {"sub": str(user.id)})

    response.set_cookie(booking_access_token, access_token, httponly=True)
    response.set_cookie(booking_refresh_token, refresh_token, httponly=True)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/refresh/",
    response_model=TokenInfo,
    response_model_exclude_none=True
)
async def refresh_jwt(
        response: Response,
        user: User = Depends(get_current_user_for_refresh)
) -> TokenInfo:
    access_token = JWTToken.create(JWTToken.ACCESS_TOKEN, {"sub": str(user.id)})
    response.set_cookie(booking_access_token, access_token, httponly=True)
    return TokenInfo(access_token=access_token)


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(booking_access_token)