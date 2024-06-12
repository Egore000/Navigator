from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.backend.hotels.router import get_hotels_by_location_and_time

from app.config import TEMPLATES


router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

tempaltes = Jinja2Templates(directory=TEMPLATES)


@router.get("/hotels")
async def get_hotels_page(
    request: Request,
    hotels=Depends(get_hotels_by_location_and_time)
):
    return tempaltes.TemplateResponse(
        name="hotels.html",
        context={
            "request": request,
            "hotels": hotels,
        }
    )
