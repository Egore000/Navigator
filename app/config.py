from pathlib import Path

from pydantic import BaseSettings


BASE_DIR = Path(__file__).parent.parent

FRONTEND_BASE_DIR = BASE_DIR / "app" / "frontend"
STATIC = FRONTEND_BASE_DIR / "static"
TEMPLATES = FRONTEND_BASE_DIR / "templates"
IMAGES = STATIC / "images"


class ProjectSettings(BaseSettings):
    class Config:
        env_file = '.env'


class AuthJWT(ProjectSettings):
    PRIVATE_KEY: Path = BASE_DIR / "certs" / "private.pem"
    PUBLIC_KEY: Path = BASE_DIR / "certs" / "public.pem"
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1


class DBSettings(ProjectSettings):
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


class SMTPSettings(ProjectSettings):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str


class RedisSettings(ProjectSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"


class Settings(ProjectSettings):
    db = DBSettings()
    auth_jwt = AuthJWT()
    smtp = SMTPSettings()
    redis = RedisSettings()


settings = Settings()

booking_access_token = "Bearer"
booking_refresh_token = "Refresh"
