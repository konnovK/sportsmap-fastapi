from fastapi import APIRouter, HTTPException, Depends, UploadFile, BackgroundTasks
from loguru import logger
from starlette.responses import JSONResponse

from api.context import AppContext
from api.dependencies import get_app_context, admin_user

import pandas as pd

from api.schema.facility import FacilitySearchRequest

router = APIRouter(
    prefix='/excel',
    tags=['Excel']
)


@router.post('/validate')
async def validate_excel(
    originFileObj: UploadFile,
    app_context: AppContext = Depends(get_app_context),
    admin_user_id: str = Depends(admin_user)

):
    excel_file = originFileObj

    xls = pd.read_excel(excel_file.file, sheet_name=None)

    facilities = app_context.excel_service.xls_to_list(xls)
    errors = app_context.excel_service.validate_excel_facilities(facilities)

    logger.debug(
        f'VALIDATE {excel_file.size / 1000 :.3f} KB EXCEL {excel_file.filename}: '
        f'{len(facilities)} FACILITIES: {len(errors)} ERRORS FOUND'
    )

    if len(errors) > 0:
        return JSONResponse({"errors": errors}, status_code=400)


@router.post('/import')
async def import_excel(
    originFileObj: UploadFile,
    background_tasks: BackgroundTasks,
    app_context: AppContext = Depends(get_app_context),
    admin_user_id: str = Depends(admin_user)
):
    excel_file = originFileObj

    xls = pd.read_excel(excel_file.file, sheet_name=None)

    facilities = app_context.excel_service.xls_to_list(xls)

    facilities_in_db = await app_context.excel_service.add_excel_facilities_to_db(facilities)

    logger.debug(
        f'IMPORT {excel_file.size / 1000:.3f} KB EXCEL: {len(facilities)} INPUT: {len(facilities_in_db)} ADDED'
    )

    if app_context.settings.YANDEX_GEOCODER_API_KEY is not None:
        yandex_api_key = app_context.settings.YANDEX_GEOCODER_API_KEY
        # TODO: в фоне сделать задачу на поход в геокодер для каждого объекта (не более 1000)
    else:
        logger.warning(f"FAILED WITH USING Yandex Geocoder")

    app_context.email_service.send_mail_to_self(
        'Был загружен Excel документ',
        f'На сайт был загружен Excel документ\n\n'
        f'Размер файла - {excel_file.size / 1000:.3f} KB\n'
        f'{len(facilities)} спортивных объектов содержал документ\n'
        f'{len(facilities_in_db)} из них было добавлено в базу данных'
    )

    return JSONResponse([str(f['id']) for f in facilities_in_db], status_code=200)


@router.post('/export')
async def export_excel(
    body: FacilitySearchRequest,
    app_context: AppContext = Depends(get_app_context),
    admin_user_id: str = Depends(admin_user)
):
    filters = body.filters
    if filters is not None:
        filters_ = []
        for f in filters:
            filters_.append(f.model_dump())
    else:
        filters_ = None

    count, facilities = await app_context.facility_service.search(
        body.all,
        body.q,
        None,
        None,
        body.order_by,
        body.order_desc,
        body.hidden,
        body.type,
        body.owning_type,
        body.covering_type,
        body.paying_type,
        body.age,
        filters_,
        body.x,
        body.y
    )
    facilities = [f.to_dict() for f in facilities]

    try:
        excel_filename = 'output.xlsx'
        app_context.excel_service.create_excel_file(excel_filename, facilities)

        with open(excel_filename, 'rb') as file_reader:
            file_bytes = file_reader.read()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='Ошибка сервера при работе с файловой системой')

    url = app_context.s3_service.s3_upload_bytes(
        file_bytes,
        excel_filename
    )
    if url is None:
        raise HTTPException(status_code=500, detail='Ошибка сервера при работе с бакетом')

    return JSONResponse({"url": url})
