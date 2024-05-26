from fastapi import APIRouter, Depends

from hotels.schemas import Hotel
from hotels.service import HotelsSearchArgs


router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get("")
def get_hotels(
    search_args: HotelsSearchArgs = Depends()
) -> list[Hotel]:
    hotels = [
        {
            "address": "пер.Буяновский, д.3А",
            "name": "Парус",
            "stars": 4
        },
        {
            "address": "ул.Пушкина, д.Колотушкина",
            "name": "Плаза-Хотел",
            "stars": 3
        },
        {
            "address": "ул.Гагарина, д.3",
            "name": "Космос",
            "stars": 5
        }
    ]
    return hotels

