import uuid

import pytest

from service.exc import FacilityAlreadyExistsServiceException, FacilityNotFoundServiceException
from service.facility_service import FacilityService


async def create_facility(facility_service_: FacilityService, facility_create_data_dict_):
    facility_create_data = facility_service_.to_facility_create_service_model(facility_create_data_dict_)
    return await facility_service_.create(facility_create_data)


async def test_facility_create_success(facility_service):
    facility_create_data = {
        "name": "test facility",
        "address": "wrhtjydsh jdgs z",
        "owner": "OOO lol kek corp",
        "area": 42.2,
        "type": "ndfgn",
        "covering_type": "гравийное",
        "paying_type": [
            "бюджетные",
            "платные"
        ],
        "age": [
            "дети",
            "dfgnb"
        ]
    }

    facility = await create_facility(facility_service, facility_create_data)
    print(facility)

    with pytest.raises(FacilityAlreadyExistsServiceException):
        await create_facility(facility_service, facility_create_data)


async def test_facility_put_unknown(facility_service):
    facility_put_data = {
        "name": "ndjpzrjhspe",
        "address": "wrhtjydsh jdgs z",
        "owner": "OOO lol kek corp",
        "area": 64.2,
        "type": "ndfgn",
        "covering_type": "гравийное",
        "paying_type": [],
        "age": [
            "взрослые"
        ]
    }

    with pytest.raises(FacilityNotFoundServiceException):
        await facility_service.put(
            uuid.uuid4(),
            facility_service.to_facility_put_service_model(facility_put_data)
        )


async def test_facility_put_success(facility_service):
    facility_create_data = {
        "name": "test facility",
        "address": "wrhtjydsh jdgs z",
        "owner": "OOO lol kek corp",
        "area": 42.2,
        "type": "ndfgn",
        "covering_type": "гравийное",
        "paying_type": [
            "бюджетные",
            "платные"
        ],
        "age": [
            "дети",
            "dfgnb"
        ]
    }
    facility_put_data = {
        "name": "ndjpzrjhspe",
        "address": "wrhtjydsh jdgs z",
        "owner": "OOO lol kek corp",
        "area": 64.2,
        "type": "ndfgn",
        "covering_type": "гравийное",
        "paying_type": [],
        "age": [
            "взрослые"
        ]
    }

    facility = await create_facility(facility_service, facility_create_data)
    print(facility)

    facility = await facility_service.put(
        facility.id,
        facility_service.to_facility_put_service_model(facility_put_data)
    )

    print(facility)


async def test_facility_patch_success(facility_service):
    facility_create_data = {
        "name": "test facility",
        "address": "wrhtjydsh jdgs z",
        "owner": "OOO lol kek corp",
        "area": 42.2,
        "type": "ndfgn",
        "covering_type": "гравийное",
        "paying_type": [
            "бюджетные",
            "платные"
        ],
        "age": [
            "дети",
            "dfgnb"
        ]
    }
    facility_patch_data = {
        "area": 64.2,
        "age": [
            "взрослые"
        ]
    }

    facility = await create_facility(facility_service, facility_create_data)
    print(facility)

    facility = await facility_service.patch(
        facility.id,
        facility_service.to_facility_patch_service_model(facility_patch_data)
    )

    print(facility)


async def test_facility_patch_already_exists(facility_service):
    facility_create_data1 = {
        "name": "test facility",
        "address": "wrhtjydsh jdgs z",
        "owner": "OOO lol kek corp",
        "area": 42.2,
        "type": "ndfgn",
        "covering_type": "гравийное",
        "paying_type": [
            "бюджетные",
            "платные"
        ],
        "age": [
            "дети",
            "dfgnb"
        ]
    }
    facility_create_data2 = {
        "name": "test facility",
        "address": "wrhtjydsh jdgs z",
        "owner": "OOO lol kek corp",
        "area": 64.2,
        "type": "ndfgn",
        "covering_type": "гравийное",
        "paying_type": [
            "бюджетные",
            "платные"
        ],
        "age": [
            "дети",
            "dfgnb"
        ]
    }
    facility_patch_data = {
        "area": 64.2
    }

    facility1 = await create_facility(facility_service, facility_create_data1)
    await create_facility(facility_service, facility_create_data2)

    with pytest.raises(FacilityAlreadyExistsServiceException):
        await facility_service.patch(
            facility1.id,
            facility_service.to_facility_patch_service_model(facility_patch_data)
        )
