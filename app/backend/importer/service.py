from datetime import datetime
import json

from app.backend.hotels.service import HotelDAO
from app.backend.hotels.rooms.service import RoomsDAO
from app.backend.bookings.service import BookingDAO

from app.logger import logger


TABLE_MODEL_MAP = {
    "hotels": HotelDAO,
    "rooms": RoomsDAO,
    "bookings": BookingDAO,
}


def convert_csv_to_pg(csv_data):
    try:
        data = []
        for row in csv_data:
            for k, v in row.items():
                if v.isdigit():
                    row[k] = int(v)
                elif k == "service":
                    row[k] = json.loads(v.replace("'", '"'))
                elif "date" in k:
                    row[k] = datetime.strptime(v, "%Y-%m-%d")
            data.append(row)
        return data
    except:
        logger.error("Cannot convert CSV to DB format", exc_info=True)
