from pathlib import Path

from pydantic import BaseSettings


BASE_DIR = Path(__file__).parent.parent

FRONTEND_BASE_DIR = BASE_DIR / "app" / "frontend"
STATIC = FRONTEND_BASE_DIR / "static"
TEMPLATES = FRONTEND_BASE_DIR / "templates"
IMAGES = STATIC / "images"


class AuthJWT(BaseSettings):
    PRIVATE_KEY: Path = BASE_DIR / "certs" / "private.pem"
    PUBLIC_KEY: Path = BASE_DIR / "certs" / "public.pem"
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1

    class Config:
        env_file = '.env'


class DBSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_PASS: int
    DB_NAME: str
    DB_USER: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://" \
               f"{self.DB_USER}:{self.DB_PASS}@" \
               f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"


class Settings(BaseSettings):
    db: DBSettings = DBSettings()

    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()

booking_access_token = "Bearer"
booking_refresh_token = "Refresh"
