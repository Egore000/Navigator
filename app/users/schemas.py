from pydantic import BaseModel, EmailStr
from app.users.dependencies import UserRole


class UserAuth(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserData(BaseModel):
    id: int
    email: EmailStr
    role: UserRole