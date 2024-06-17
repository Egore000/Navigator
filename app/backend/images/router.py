import shutil

from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse

from app.backend.responses import CreatedSuccessfullyResponse
from app.backend.tasks.tasks import process_picture
from app.config import IMAGES

router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок", ],
)


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile) -> JSONResponse:
    path = IMAGES / f"{name}.webp"
    with open(path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_picture.delay(str(path))
    return CreatedSuccessfullyResponse
