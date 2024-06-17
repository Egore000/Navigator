import sentry_sdk

from app.config import settings


def init_sentry():
    sentry_sdk.init(
        dsn=settings.logging.SENTRY_URL,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )