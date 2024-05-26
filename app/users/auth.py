import datetime
from passlib.context import CryptContext
from jose import jwt
from pydantic import EmailStr

from users.models import Users
from users.service import UsersService
from config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM 
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str) -> Users|None:
    user = await UsersService.get_one_or_none(email=email)
    if user and verify_password(password, user.hashed_password):
        return user
    