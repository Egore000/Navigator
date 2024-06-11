from datetime import date, datetime, timedelta
from fastapi import APIRouter, Query

from app import exceptions
from app.core.utils import validate_date
from app.hotels.schemas import HotelScheme, HotelInfo
from app.hotels.service import HotelDAO


router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get("")
async def get_all_hotels() -> list[HotelScheme]:
    """Вывод всех отелей из БД"""
    return await HotelDAO.get_all()


@router.get("/{location}")
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например, {datetime.now().date() + timedelta(days=1)}"),
) -> list[HotelInfo]:
    """Поиск отелей по местоположению и времени"""
    validate_date(date_from, date_to)

    hotels = await HotelDAO.search_for_hotels(location, date_from, date_to)

    if not hotels:
        raise exceptions.NotFoundError
    return hotels


@router.get("/id/{hotel_id}", response_model_exclude_none=True)
async def get_hotel_by_id(hotel_id: int) -> HotelInfo:
    """Информация о конкретном отеле"""
    hotel = await HotelDAO.get_one_or_none(id=hotel_id)

    if not hotel:
        raise exceptions.NotFoundError
    return hotel
