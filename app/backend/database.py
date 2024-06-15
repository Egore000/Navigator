from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


if settings.project.MODE == "TEST":
    DATABASE_URL = settings.test_db.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.db.DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(url=DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Model(DeclarativeBase):
    pass
