from datetime import datetime, timedelta, UTC
from typing import Any, Literal

import jwt
import bcrypt

from pydantic import EmailStr

from app import exceptions
from app.config import settings

from app.users.models import User
from app.users.service import UsersService


def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )


async def authenticate_user(email: EmailStr, password: str) -> User | None:
    user = await UsersService.get_one_or_none(email=email)
    if user and verify_password(password, user.hashed_password):
        return user


class JWTToken:
    PRIVATE_KEY = settings.auth_jwt.PRIVATE_KEY.read_text()
    PUBLIC_KEY = settings.auth_jwt.PUBLIC_KEY.read_text()
    ALGORITHM = settings.auth_jwt.ALGORITHM
    TOKEN_TYPE_FIELD = "type"
    ACCESS_TOKEN_EXPIRE_TIME = settings.auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_TIME = settings.auth_jwt.REFRESH_TOKEN_EXPIRE_DAYS
    ACCESS_TOKEN = "access"
    REFRESH_TOKEN = "refresh"

    @classmethod
    def create(cls, token_type: Literal["access", "refresh"], payload: dict) -> str:
        to_encode = payload.copy()

        if token_type == cls.ACCESS_TOKEN:
            delta = timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_TIME)
        elif token_type == cls.REFRESH_TOKEN:
            delta = timedelta(days=cls.REFRESH_TOKEN_EXPIRE_TIME)
        else:
            raise exceptions.IncorrectTokenTypeError(
                "Запрос на получение токена несуществующего типа"
            )

        now = datetime.now(UTC)
        expire = now + delta
        to_encode.update({
            cls.TOKEN_TYPE_FIELD: token_type,
            "exp": expire,
            "iat": now,
        })

        token = cls.encode(to_encode)
        return token

    @classmethod
    def encode(cls, payload: dict[str, Any]) -> str:
        return jwt.encode(payload, cls.PRIVATE_KEY, cls.ALGORITHM)

    @classmethod
    def decode(cls, token: str | bytes) -> dict:
        return jwt.decode(token, cls.PUBLIC_KEY, algorithms=[cls.ALGORITHM,])

    @classmethod
    def validate(cls, token_type: str, payload: dict) -> bool:
        current_token_type = payload.get(cls.TOKEN_TYPE_FIELD)
        if current_token_type == token_type:
            return True
        raise exceptions.IncorrectTokenError

    @classmethod
    def get_payload(cls, token: str) -> dict:
        try:
            payload = JWTToken.decode(token)
        except jwt.exceptions.InvalidTokenError:
            raise exceptions.IncorrectTokenFormatException
        return payload
