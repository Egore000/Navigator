from pydantic import BaseModel


class RoomScheme(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str | None
    services: list[str | None]
    price: int
    quantity: int
    image_id: int


class RoomInfo(RoomScheme):
    total_cost: int
    rooms_left: int
