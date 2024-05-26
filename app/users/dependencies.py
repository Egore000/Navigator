from datetime import datetime, UTC

from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError

from users.models import Users
from users.service import UsersService
from config import settings, booking_access_token



def get_token(request: Request):
    token = request.cookies.get(booking_access_token)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_user(token: str = Depends(get_token)) -> Users:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(UTC).timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await UsersService.get_one_or_none(id=int(user_id))
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return user


async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return current_user