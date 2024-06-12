import shutil

from fastapi import APIRouter, UploadFile

from app.config import IMAGES


router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок", ],
)


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    with open(IMAGES / f"{name}.webp", "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
