from service.facility_enum_service import FacilityEnumService


async def test_facility_enum_get_all_facility_types_success(facility_enum_service: FacilityEnumService):
    print(await facility_enum_service.get_all_facility_types())


async def test_facility_enum_get_all_facility_owning_types_success(facility_enum_service: FacilityEnumService):
    print(await facility_enum_service.get_all_facility_owning_types())


async def test_facility_enum_get_all_facility_covering_types_success(facility_enum_service: FacilityEnumService):
    print(await facility_enum_service.get_all_facility_covering_types())


async def test_facility_enum_get_all_facility_paying_types_success(facility_enum_service: FacilityEnumService):
    print(await facility_enum_service.get_all_facility_paying_types())


async def test_facility_enum_get_all_facility_ages_success(facility_enum_service: FacilityEnumService):
    print(await facility_enum_service.get_all_facility_ages())
