from api.app import create_app
from db.db import DB
from service.email_service import EmailService
from service.facility_enum_service import FacilityEnumService
from service.facility_service import FacilityService
from service.user_service import UserService
from settings import Settings

from fastapi.testclient import TestClient
import pytest


@pytest.fixture()
def settings():
    settings = Settings.new()
    settings.API_DB_URL = settings.API_TEST_DB_URL
    yield settings


@pytest.fixture()
async def db(settings):
    db = DB(settings)
    await db.recreate_tables()
    await db.create_all_enums()
    await db.create_super_user()
    yield db


@pytest.fixture()
async def user_service(db):
    yield UserService(async_session=db.async_session)


@pytest.fixture()
async def facility_service(db):
    yield FacilityService(async_session=db.async_session)


@pytest.fixture()
async def facility_enum_service(db):
    yield FacilityEnumService(async_session=db.async_session)


@pytest.fixture()
async def email_service(db, settings):
    yield EmailService(async_session=db.async_session, settings=settings)


@pytest.fixture()
async def app(settings, db):
    app = create_app()

    from api.context import AppContext
    app_context = AppContext(settings)

    from api import globals
    globals.settings = settings
    globals.app_context = app_context

    print(globals.settings)
    yield app


@pytest.fixture()
async def client(app):
    yield TestClient(app)
