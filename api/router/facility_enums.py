from fastapi import APIRouter, Depends

from api.context import AppContext
from api.dependencies import get_app_context
from api.schema.facility_enums import FacilityTypeResponse

router = APIRouter(
    prefix='',
    tags=['FacilityEnum']
)


@router.get('/facility-type', tags=['FacilityType'])
async def get_all_facility_types(app_context: AppContext = Depends(get_app_context)) -> FacilityTypeResponse:
    facility_types = await app_context.facility_enum_service.get_all_facility_types()
    return FacilityTypeResponse(data=[f.name for f in facility_types])


@router.get('/facility-owning-type', tags=['FacilityOwningType'])
async def get_all_facility_owning_types(app_context: AppContext = Depends(get_app_context)) -> FacilityTypeResponse:
    facility_types = await app_context.facility_enum_service.get_all_facility_owning_types()
    return FacilityTypeResponse(data=[f.name for f in facility_types])


@router.get('/facility-covering-type', tags=['FacilityCoveringType'])
async def get_all_facility_covering_types(app_context: AppContext = Depends(get_app_context)) -> FacilityTypeResponse:
    facility_types = await app_context.facility_enum_service.get_all_facility_covering_types()
    return FacilityTypeResponse(data=[f.name for f in facility_types])


@router.get('/facility-paying-type', tags=['FacilityPayingType'])
async def get_all_facility_paying_types(app_context: AppContext = Depends(get_app_context)) -> FacilityTypeResponse:
    facility_types = await app_context.facility_enum_service.get_all_facility_paying_types()
    return FacilityTypeResponse(data=[f.name for f in facility_types])


@router.get('/facility-age', tags=['FacilityAge'])
async def get_all_facility_ages(app_context: AppContext = Depends(get_app_context)) -> FacilityTypeResponse:
    facility_types = await app_context.facility_enum_service.get_all_facility_ages()
    return FacilityTypeResponse(data=[f.name for f in facility_types])
