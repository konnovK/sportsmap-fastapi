import uuid

from fastapi import APIRouter, Depends
from loguru import logger

from api.context import AppContext
from api.dependencies import get_app_context, admin_user
from api.schema.facility import FacilityRequest, FacilityResponse, FacilityPatchRequest, FacilitySearchRequest, \
    FacilitySearchResponse

router = APIRouter(
    prefix='/facility',
    tags=['Facility']
)


@router.post('', status_code=201)
async def create_facility(
        body: FacilityRequest,
        admin_user_id: str = Depends(admin_user),
        app_context: AppContext = Depends(get_app_context),

) -> FacilityResponse:
    facility = await app_context.facility_service.create(body)

    app_context.email_service.send_mail_to_self(
        "Был создан новый спортивный объект",
        f"На сайте был создан новый спортивный объект:\n\n"
        f"Название - {facility.name}\n"
        f"Адрес - {facility.address}\n"
        f"Пользователь - {facility.owner}\n"
        f"Тип объекта - {facility.type.name}"
    )

    return FacilityResponse.from_service_model(facility)


@router.put('/{id}')
async def fully_update_facility(
        id: uuid.UUID,
        body: FacilityRequest,
        admin_user_id: str = Depends(admin_user),
        app_context: AppContext = Depends(get_app_context),
) -> FacilityResponse:
    facility = await app_context.facility_service.put(id, body)
    return FacilityResponse.from_service_model(facility)


@router.patch('/{id}')
async def partial_update_facility(
        id: uuid.UUID,
        body: FacilityPatchRequest,
        admin_user_id: str = Depends(admin_user),
        app_context: AppContext = Depends(get_app_context),
) -> FacilityResponse:
    body_dict = body.model_dump()
    body_without_none = dict()
    for k, v in body_dict.items():
        if v is not None:
            body_without_none[k] = v
    facility = await app_context.facility_service.patch(
        id,
        app_context.facility_service.to_facility_patch_service_model(body_without_none)
    )
    return FacilityResponse.from_service_model(facility)


@router.delete('/{id}', status_code=204)
async def delete_facility(
        id: uuid.UUID,
        admin_user_id: str = Depends(admin_user),
        app_context: AppContext = Depends(get_app_context),
):
    await app_context.facility_service.delete(id)


@router.get('/{id}')
async def get_facility_by_id(
        id: uuid.UUID,
        app_context: AppContext = Depends(get_app_context),
) -> FacilityResponse:
    facility = await app_context.facility_service.get_by_id(id)
    return FacilityResponse.from_service_model(facility)


@router.post('/search')
async def search_facility(
        body: FacilitySearchRequest,
        app_context: AppContext = Depends(get_app_context),
) -> FacilitySearchResponse:
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
        body.limit,
        body.offset,
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
    facilities_resp = []
    for f in facilities:
        facilities_resp.append(FacilityResponse.from_service_model(f))

    logger.debug(f"SEARCH: {len(facilities)} FACILITIES")

    return FacilitySearchResponse(
        count=count,
        facilities=facilities_resp
    )
