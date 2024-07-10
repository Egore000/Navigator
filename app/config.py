import os
from pathlib import Path
from typing import Literal

from pydantic import BaseSettings

BASE_DIR = Path(__file__).parent.parent

FRONTEND_BASE_DIR = BASE_DIR / "app" / "frontend"
STATIC = FRONTEND_BASE_DIR / "static"
TEMPLATES = FRONTEND_BASE_DIR / "templates"
IMAGES = STATIC / "images"

LOG_DIR = BASE_DIR / "logs"


class Config(BaseSettings):
    class Config:
        env_file = '.env'


class ProjectSettings(Config):
    MODE: Literal["DEV", "TEST", "PROD"]


class LoggingSettings(Config):
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    SENTRY_URL: str
    DIR: Path = LOG_DIR


class AuthJWT(Config):
    PRIVATE_KEY: Path = BASE_DIR / "certs" / "private.pem"
    PUBLIC_KEY: Path = BASE_DIR / "certs" / "public.pem"
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


class DBSettings(Config):
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


class TestDBSettings(Config):
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_PASS: int
    TEST_DB_NAME: str
    TEST_DB_USER: str

    @property
    def TEST_DATABASE_URL(self):
        return f"postgresql+asyncpg://" \
               f"{self.TEST_DB_USER}:{self.TEST_DB_PASS}@" \
               f"{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"


class SMTPSettings(Config):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str


class RedisSettings(Config):
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"


class Settings(Config):
    project = ProjectSettings()
    db = DBSettings()
    test_db = TestDBSettings()
    auth_jwt = AuthJWT()
    smtp = SMTPSettings()
    redis = RedisSettings()
    logging = LoggingSettings()


settings = Settings()

os.chmod(settings.logging.DIR, 0o777)

booking_access_token = "Bearer"
booking_refresh_token = "Refresh"
