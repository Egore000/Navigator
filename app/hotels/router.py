from datetime import date
from fastapi import APIRouter, Depends, Query

from hotels.schemas import Hotel
from hotels.service import HotelsSearchArgs, HotelService


router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get("")
async def get_all_hotels():
    return await HotelService.get_all()


@router.get("/{location}")
async def get_hotels_by_location(
    search_args: HotelsSearchArgs = Depends()
):
    return await HotelService.get_all_by_location(
        search_args.location,
        search_args.date_from,
        search_args.date_to,
    )


@router.get("/id/{hotel_id}")
async def get_hotel_by_id(
    hotel_id: int
):
    return await HotelService.get_one_or_none(id=hotel_id)