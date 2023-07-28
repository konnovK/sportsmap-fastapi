import time
import uuid

from fastapi import APIRouter, Depends, UploadFile

from api.context import AppContext
from api.dependencies import get_app_context, admin_user
from api.schema.photo import PhotoResponse

router = APIRouter(
    prefix='',
    tags=['Photo']
)


@router.post('/facility/{id}/photo')
async def create_facility_photo(
    id: uuid.UUID,
    originFileObj: UploadFile,
    app_context: AppContext = Depends(get_app_context),
    admin_user_id: str = Depends(admin_user)
) -> PhotoResponse:
    photo_file = originFileObj
    filename = photo_file.filename
    key = f'{id}-{int(time.time())}-{filename}'
    url = app_context.s3_service.s3_upload_bytes(photo_file.file.read(), key)
    photo = await app_context.photo_service.create(url, key, id)
    return photo


@router.delete('/facility/{facility_id}/photo/{photo_id}')
async def delete_facility_photo(
    facility_id: uuid.UUID,
    photo_id: uuid.UUID,
    app_context: AppContext = Depends(get_app_context),
    admin_user_id: str = Depends(admin_user)
):
    photo_filename = await app_context.photo_service.delete(facility_id, photo_id)
    app_context.s3_service.s3_delete_elem(photo_filename)
