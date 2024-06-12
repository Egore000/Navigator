from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_hotels_by_location_and_time


router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

tempaltes = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
async def get_hotels_page(
    request: Request,
    hotels=Depends(get_hotels_by_location_and_time)
):
    return tempaltes.TemplateResponse(
        name="hotels.html",
        context={
            "request": request,
            "hotels": hotels
        }
    )