from pydantic import BaseModel, EmailStr

from app.config import booking_access_token
from app.users.permissions import UserRole


class UserData(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
