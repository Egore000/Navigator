from pydantic import BaseModel, EmailStr

from app.config import booking_access_token


class UserAuth(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = booking_access_token
