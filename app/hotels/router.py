from datetime import date, datetime, timedelta
from fastapi import APIRouter, Query

from app.hotels.schemas import HotelScheme
from app.hotels.service import HotelService


router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get("")
async def get_all_hotels():
    return await HotelService.get_all()


@router.get("/{location}")
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например, {datetime.now().date() + timedelta(days=1)}"),
):
    return await HotelService.search_for_hotels(location, date_from, date_to)


@router.get("/id/{hotel_id}")
async def get_hotel_by_id(
    hotel_id: int
):
    return await HotelService.get_one_or_none(id=hotel_id)
