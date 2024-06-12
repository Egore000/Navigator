from datetime import datetime, UTC

from fastapi import Depends, Request

from app import exceptions
from app.config import booking_access_token, booking_refresh_token

from app.users.models import User
from app.users.service import UsersDAO
from app.users.auth.auth import JWTToken


def get_token(token_field: str):
    """Получение нужного токена ('access'/'refresh') из cookies"""
    def wrapper(request: Request) -> str:
        token = request.cookies.get(token_field)
        if not token:
            raise exceptions.TokenAbsentException
        return token
    return wrapper


async def get_user_by_token(payload: dict) -> User:
    """Получение пользователя по токену"""
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(UTC).timestamp()):
        raise exceptions.TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise exceptions.UserDoesNotExistsException

    user = await UsersDAO.get_one_or_none(id=int(user_id))
    if not user:
        raise exceptions.UserDoesNotExistsException
    return user


def get_user(token_type: str, token_field: str):
    """
    Декоратор для получения пользователя по нужному токену
    token_type - тип токена (access/refresh)
    token_field - поле в cookies с нужным токеном
    """
    async def wrapper(token: str = Depends(get_token(token_field))) -> User:
        payload = JWTToken.get_payload(token)
        JWTToken.validate(token_type, payload)
        return await get_user_by_token(payload)
    return wrapper


get_current_user = get_user(JWTToken.ACCESS_TOKEN, booking_access_token)
get_current_user_for_refresh = get_user(JWTToken.REFRESH_TOKEN,
                                        booking_refresh_token)
