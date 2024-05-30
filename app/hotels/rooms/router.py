from fastapi import APIRouter

from hotels.rooms.models import Rooms
from hotels.rooms.service import RoomsService


router = APIRouter(
    prefix="/hotel/{hotel_id}/rooms",
    tags=["Комнаты"]   
)


@router.get("")
async def get_rooms(
    hotel_id: int
):
    return await RoomsService.get_all(hotel_id)