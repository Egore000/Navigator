from typing import Literal
import codecs
import csv

from fastapi import APIRouter, UploadFile, Depends

from app.backend.importer.service import TABLE_MODEL_MAP, convert_csv_to_pg
from app.backend import exceptions
from app.backend.users.permissions import get_current_admin_user

router = APIRouter(
    prefix="/import",
    tags=["Загрузка"]
)


@router.post(
    "/{table_name}",
    status_code=201,
    dependencies=[Depends(get_current_admin_user),],
)
async def import_data(
        table_name: Literal["hotels", "rooms", "bookings"],
        file: UploadFile
):
    """Загрузка данных в таблицу table_name"""
    ModelDAO = TABLE_MODEL_MAP[table_name]

    csv_reader = csv.DictReader(
        codecs.iterdecode(
            file.file,
            encoding="utf-8"
        ),
        delimiter=";"
    )
    data = convert_csv_to_pg(csv_reader)
    file.file.close()

    if not data:
        raise exceptions.CannotProcessCSVFileError
    added_data = await ModelDAO.add_bulk(data)

    if not added_data:
        raise exceptions.CannotAddDataToDatabaseError
