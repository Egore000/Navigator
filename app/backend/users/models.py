from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.backend.database import Model


class User(Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=True, default='user')

    booking = relationship("Bookings", back_populates="user")

    def __str__(self):
        return self.email
