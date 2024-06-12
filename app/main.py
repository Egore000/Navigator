from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import uvicorn

from app.backend.core.utils import lifespan

from app.backend.users.auth.router import router as router_auth
from app.backend.users.router import router as router_users
from app.backend.bookings.router import router as router_bookings
from app.backend.hotels.router import router as router_hotels
from app.backend.hotels.rooms.router import router as router_rooms

from app.backend.pages.router import router as router_pages
from app.backend.images.router import router as router_images

from app.config import STATIC


app = FastAPI(lifespan=lifespan)

app.mount("/static",
          StaticFiles(directory=STATIC),
          name="static")

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)

app.include_router(router_pages)
app.include_router(router_images)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "OPTIONS", "PATCH", "DELETE"],
    allow_headers=[
        "Content-type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Allow-Control-Allow-Origin",
        "Authorization"
    ],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
