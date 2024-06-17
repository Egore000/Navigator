from sqlalchemy import MappingResult, insert, select, update, ScalarResult

from app.backend.exceptions import NotFoundError
from app.backend.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        result: MappingResult = await cls.filter(**filter_by)
        return result.one_or_none()

    @classmethod
    async def get_all(cls, **filter_by):
        result: MappingResult = await cls.filter(**filter_by)
        return result.all()

    @classmethod
    async def delete(cls, item_id: int):
        async with async_session_maker() as session:
            data = await session.get(cls.model, item_id)
            if not data:
                raise NotFoundError
            await session.delete(data)
            await session.commit()

    @classmethod
    async def update(cls, item_id: int, **values) -> ScalarResult:
        query = (
            update(cls.model)
            .where(cls.model.id == item_id)
            .values(**values)
            .returning(cls.model)
        )
        result = await cls.commit(query)
        return result.scalar()

    @classmethod
    async def insert(cls, **data):
        query = (
            insert(cls.model)
            .values(**data)
            .returning(cls.model)
        )
        result = await cls.commit(query)
        return result

    @classmethod
    async def filter(cls, **filter_by) -> MappingResult:
        query = (
            select(cls.model.__table__.columns)
            .filter_by(**filter_by)
        )
        result = await cls.execute(query)
        return result.mappings()

    @classmethod
    async def execute(cls, query):
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result

    @classmethod
    async def commit(cls, query):
        async with async_session_maker() as session:
            result = await session.execute(query)
            await session.commit()
            return result


