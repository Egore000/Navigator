from sqlalchemy import MappingResult, insert, select

from database import async_session_maker



class BaseService:
    model = None

    @classmethod
    async def __get_query_result(cls, **filter_by) -> MappingResult:
        async with async_session_maker() as session:
            query = select(
                cls.model.__table__.columns
            ).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings()
        
    @classmethod
    async def __insert_data(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        result: MappingResult = await cls.__get_query_result(**filter_by)
        return result.one_or_none()
    
    @classmethod
    async def get_all(cls, **filter_by):
        result: MappingResult = await cls.__get_query_result(**filter_by)
        return result.all()
    
    @classmethod
    async def add(cls, **data):
        await cls.__insert_data(**data)