from pydantic import BaseModel, EmailStr

from app.users.permissions import UserRole


class UserData(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
