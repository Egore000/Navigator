import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin

from app.backend.admin.auth import authentication_backend
from app.backend.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UserAdmin
from app.backend.bookings.router import router as router_bookings
from app.backend.core.utils import lifespan
from app.backend.database import engine
from app.backend.hotels.rooms.router import router as router_rooms
from app.backend.hotels.router import router as router_hotels
from app.backend.images.router import router as router_images
from app.backend.pages.router import router as router_pages
from app.backend.users.auth.router import router as router_auth
from app.backend.users.router import router as router_users
from app.config import STATIC
from app.middlewares import LoggingMiddleware

# init_sentry()

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
app.add_middleware(LoggingMiddleware)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
