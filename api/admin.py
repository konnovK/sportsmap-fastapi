import os
from hashlib import md5
from typing import Optional
from fastapi import FastAPI
from api.globals import settings, app_context

from loguru import logger
from sqladmin import Admin, ModelView

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from db.model.user import User
from db.model.facility import (
    Facility,
    FacilityType,
    FacilityOwningType,
    FacilityCoveringType,
    FacilityPayingType,
    FacilityAge,
    FacilityPhoto
)


def _encode_token(email: str, password: str):
    return md5(f'{email}:{password}'.encode()).hexdigest()


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # Validate username/password credentials
        # And update session
        if username == settings.API_SUPERUSER_EMAIL and password == settings.API_SUPERUSER_PASSWORD:
            token = _encode_token(username, password)
            request.session.update({"token": token})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if token != _encode_token(settings.API_SUPERUSER_EMAIL, settings.API_SUPERUSER_PASSWORD):
            return RedirectResponse(request.url_for("admin:login"), status_code=302)


def setup_admin(app: FastAPI):
    logger.debug(f"[{os.getpid()}] SETUP ADMIN FOR APP")

    authentication_backend = AdminAuth(
        secret_key=_encode_token(
            settings.API_SUPERUSER_EMAIL, settings.API_SUPERUSER_PASSWORD
        )
    )

    admin = Admin(
        app,
        app_context.db.engine,
        authentication_backend=authentication_backend,
        title="KLogger Admin"
    )

    logger.debug(f"[{os.getpid()}] REGISTER ALL DB TABLES IN ADMIN")

    class UserAdmin(ModelView, model=User):
        icon = 'fa-solid fa-user'
        can_edit = False
        can_create = False
        can_delete = False
        column_list = [User.email, User.id, User.created_at]
        column_details_exclude_list = [User.password_hash]
    admin.add_view(UserAdmin)

    class FacilityAdmin(ModelView, model=Facility):
        icon = "fa-solid fa-file"
        page_size = 50
        column_sortable_list = [Facility.created_at]
        column_searchable_list = [Facility.name, Facility.address, Facility.owner]
        column_list = [Facility.name, Facility.address, Facility.owner, Facility.type, Facility.id, Facility.created_at]
    admin.add_view(FacilityAdmin)

    class FacilityTypeAdmin(ModelView, model=FacilityType):
        icon = "fa-solid fa-tag"
        column_details_exclude_list = [FacilityType.facilities]
        column_list = [FacilityType.name]
    admin.add_view(FacilityTypeAdmin)

    class FacilityOwningTypeAdmin(ModelView, model=FacilityOwningType):
        icon = "fa-solid fa-tag"
        column_details_exclude_list = [FacilityOwningType.facilities]
        column_list = [FacilityOwningType.name]
    admin.add_view(FacilityOwningTypeAdmin)

    class FacilityCoveringTypeAdmin(ModelView, model=FacilityCoveringType):
        icon = "fa-solid fa-tag"
        column_details_exclude_list = [FacilityCoveringType.facilities]
        column_list = [FacilityCoveringType.name]
    admin.add_view(FacilityCoveringTypeAdmin)

    class FacilityPayingTypeAdmin(ModelView, model=FacilityPayingType):
        icon = "fa-solid fa-tag"
        column_details_exclude_list = [FacilityPayingType.facilities]
        column_list = [FacilityPayingType.name]
    admin.add_view(FacilityPayingTypeAdmin)

    class FacilityAgeAdmin(ModelView, model=FacilityAge):
        icon = "fa-solid fa-tag"
        column_details_exclude_list = [FacilityAge.facilities]
        column_list = [FacilityAge.name]
    admin.add_view(FacilityAgeAdmin)

    class FacilityPhotoAdmin(ModelView, model=FacilityPhoto):
        icon = "fa-solid fa-tag"
        can_create = False
        column_details_exclude_list = [FacilityPhoto.facilities]
        column_list = [FacilityPhoto.url, FacilityPhoto.id]
    admin.add_view(FacilityPhotoAdmin)


__all__ = [
    setup_admin
]
