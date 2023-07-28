import os
import uuid

from loguru import logger

from db.db import DB
from service.email_service import EmailService
from service.excel_service import ExcelService
from service.facility_enum_service import FacilityEnumService
from service.facility_service import FacilityService
from service.s3_service import S3Service
from service.user_service import UserService
from settings import Settings


class AppContext:
    def __init__(self, settings: Settings):
        self.id = uuid.uuid4()

        logger.info(f'[{os.getpid()}] INIT AppContext {self.id}')

        self.settings: Settings = settings

        self.db: DB = DB(settings=settings)

        self.user_service: UserService = UserService(async_session=self.db.async_session)
        self.facility_service: FacilityService = FacilityService(async_session=self.db.async_session)
        self.facility_enum_service = FacilityEnumService(async_session=self.db.async_session)
        self.email_service: EmailService = EmailService(async_session=self.db.async_session, settings=settings)
        self.excel_service: ExcelService = ExcelService(async_session=self.db.async_session)
        self.s3_service: S3Service = S3Service(settings=settings, bucket='sportsmap.spb.ru')
