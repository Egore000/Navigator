from fastapi import APIRouter, Depends, HTTPException, Response, status

from users.dependencies import get_current_admin_user, get_current_user
from users.auth import authenticate_user, create_access_token, get_password_hash, verify_password
from users.schemas import UserAuth
from users.models import User
from users.service import UsersService

from config import booking_access_token
import exceptions


router = APIRouter(
    prefix='/auth',
    tags=['Auth & Пользователи']
)


@router.post("/register")
async def register_user(user_data: UserAuth):
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
    user_data: UserAuth
):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise exceptions.IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(booking_access_token, access_token, httponly=True)
    return {"access_token": access_token }


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(booking_access_token)


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/all")
async def read_users_all(current_user: User = Depends(get_current_admin_user)):
    return await UsersService.get_all()