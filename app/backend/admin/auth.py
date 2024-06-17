from pydantic import EmailStr
from sqladmin.authentication import AuthenticationBackend
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.backend import exceptions
from app.backend.users.auth.auth import JWTToken, authenticate_user
from app.backend.users.auth.dependencies import get_current_user
from app.backend.users.permissions import UserRole
from app.config import settings
from app.logger import logger


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await authenticate_user(EmailStr(email), password)
        if user:
            if user.role not in (UserRole.admin, UserRole.moderator):
                raise exceptions.AccessForbiddenException

            access_token = JWTToken.create(JWTToken.ACCESS_TOKEN, {"sub": str(user.id)})
            request.session.update({"token": access_token})

            logger.info("Admin user login", extra={
                "user": email,
            })
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request):
        token = request.session.get("token")

        if not token:
            return RedirectResponse(
                request.url_for("admin:login"), status_code=status.HTTP_302_FOUND
            )

        user = await get_current_user(token)
        if not user:
            return RedirectResponse(
                request.url_for("admin:login"), status_code=status.HTTP_302_FOUND
            )

        if user.role not in (UserRole.admin, UserRole.moderator):
            raise exceptions.AccessForbiddenException

        return True


authentication_backend = AdminAuth(secret_key=settings.auth_jwt.PRIVATE_KEY)
