from datetime import datetime, UTC

from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError

from users.models import User
from users.service import UsersService

from config import settings, booking_access_token
import exceptions



def get_token(request: Request) -> str:
    token = request.cookies.get(booking_access_token)
    if not token:
        raise exceptions.TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise exceptions.IncorrectTokenFormatException
    
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(UTC).timestamp()):
        raise exceptions.TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise exceptions.UserDoesNotExistsException
    
    user = await UsersService.get_one_or_none(id=int(user_id))
    if not user:
        raise exceptions.UserDoesNotExistsException
    
    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise exceptions.AccessForbiddenException
    
    return current_user