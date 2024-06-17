from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta
from typing import Any

import fastapi
from fastapi import Query
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from pydantic import BaseModel
from redis import asyncio as aioredis

from app.backend import exceptions
from app.config import settings
from app.logger import logger


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    redis = aioredis.from_url(settings.redis.url, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    logger.info("Redis connected")
    yield


def validate_date(date_from: date, date_to: date):
    if date_from > date_to:
        raise exceptions.InvalidDateError


def return_or_raise_error(some: Any) -> Any:
    if not some:
        raise exceptions.NotFoundError
    return some


today = datetime.now().date()
tomorrow = today + timedelta(days=1)


class Dates(BaseModel):
    date_from: date = Query(
        ...,
        description=f"Например, {today}"
    )
    date_to: date = Query(
        ...,
        description=f"Например, {tomorrow}"
    )
