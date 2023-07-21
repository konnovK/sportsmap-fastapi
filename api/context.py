from loguru import logger

from db.db import DB
from service.email_service import EmailService
from service.excel_service import ExcelService
from service.facility_service import FacilityService
from service.user_service import UserService
from settings import Settings


class AppContext:
    def __init__(self, settings: Settings):
        logger.debug('INIT AppContext')
        self.settings = settings

        self.db = DB(settings=settings)

        self.user_service = UserService(async_session=self.db.async_session)
        self.facility_service = FacilityService(async_session=self.db.async_session)
        self.email_service = EmailService(async_session=self.db.async_session, settings=settings)
        self.excel_service = ExcelService(async_session=self.db.async_session)
