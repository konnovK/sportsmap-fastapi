import yandexcloud
from loguru import logger

from api.context import AppContext
from api.utils.logger import YandexHandler
from settings import Settings

settings = Settings.new()

if settings.YANDEX_CLOUD_LOGGING_OAUTH is not None and settings.YANDEX_CLOUD_LOGGING_LOG_GROUP_ID is not None:
    sdk = yandexcloud.SDK(token=settings.YANDEX_CLOUD_LOGGING_OAUTH)
    handler = YandexHandler(sdk, settings.YANDEX_CLOUD_LOGGING_LOG_GROUP_ID)
    logger.add(handler, format="{message}")
else:
    logger.warning("FAILED SETUP YandexCloud Logger")

app_context = AppContext(settings)

__all__ = [
    settings,
    app_context
]
