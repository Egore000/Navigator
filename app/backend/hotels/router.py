from datetime import date
from fastapi import APIRouter, Query

from app.backend.core.utils import validate_date, return_or_raise_error,\
    today, tomorrow
from app.backend.hotels.schemas import HotelScheme, HotelInfo
from app.backend.hotels.service import HotelDAO


router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get("")
async def get_all_hotels() -> list[HotelScheme]:
    """Вывод всех отелей из БД"""
    hotels = await HotelDAO.get_all()
    return return_or_raise_error(hotels)


@router.get("/{location}")
async def get_hotels_by_location_and_time(
        location: str,
        date_from: date = Query(
            ...,
            description=f"Например, {today}"
        ),
        date_to: date = Query(
            ...,
            description=f"Например, {tomorrow}"
        ),
) -> list[HotelInfo]:
    """Поиск отелей по местоположению и времени"""
    validate_date(date_from, date_to)
    hotels = await HotelDAO.search_for_hotels(location, date_from, date_to)
    return return_or_raise_error(hotels)


@router.get("/id/{hotel_id}", response_model_exclude_none=True)
async def get_hotel_by_id(hotel_id: int) -> HotelInfo:
    """Информация о конкретном отеле"""
    hotel = await HotelDAO.get_one_or_none(id=hotel_id)
    return return_or_raise_error(hotel)
