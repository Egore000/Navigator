from pydantic import BaseModel, EmailStr

from app.backend.users.permissions import UserRole


class UserData(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
