import uuid

from pydantic import BaseModel, ConfigDict, field_validator

from service.model.facility_model import FacilityServiceModel

EMPTY_WORKING_HOURS = {
    "monday": {
        "open": False
    },
    "tuesday": {
        "open": False
    },
    "wednesday": {
        "open": False
    },
    "thursday": {
        "open": False
    },
    "friday": {
        "open": False
    },
    "saturday": {
        "open": False
    },
    "sunday": {
        "open": False
    }
}


class FacilityWorkingHoursItem(BaseModel):
    open: bool
    all_day: bool | None = None
    since: str | None = None
    to: str | None = None


class FacilityWorkingHours(BaseModel):
    monday: FacilityWorkingHoursItem
    tuesday: FacilityWorkingHoursItem
    wednesday: FacilityWorkingHoursItem
    thursday: FacilityWorkingHoursItem
    friday: FacilityWorkingHoursItem
    saturday: FacilityWorkingHoursItem
    sunday: FacilityWorkingHoursItem


class FacilityRequest(BaseModel):
    name: str
    owner: str
    address: str

    x: float | None = None
    y: float | None = None
    hidden: bool = True

    length: float | None = None
    width: float | None = None
    height: float | None = None
    depth: float | None = None
    area: float
    eps: int | None = None
    actual_workload: int | None = None
    annual_capacity: int | None = None

    accessibility: bool = False

    site: str | None = None
    phone_number: str | None = None
    document: str | int | None = None
    note: str | None = None

    working_hours: dict | None = None

    type: str
    owning_type: str = 'другая'
    covering_type: str | None = None
    paying_type: list[str] = []
    age: list[str] = []

    @field_validator('working_hours')
    @classmethod
    def working_hours_validator(cls, v: dict) -> dict:
        FacilityWorkingHours.model_validate(v)
        return v


class FacilityPatchRequest(BaseModel):
    # изменяются отдельные поля
    name: str | None = None
    owner: str | None = None
    address: str | None = None

    x: float | None = None
    y: float | None = None
    hidden: bool | None = None

    length: float | None = None
    width: float | None = None
    height: float | None = None
    depth: float | None = None
    area: float | None = None
    eps: int | None = None
    actual_workload: int | None = None
    annual_capacity: int | None = None

    accessibility: bool | None = None

    site: str | None = None
    phone_number: str | None = None
    document: str | int | None = None
    note: str | None = None

    working_hours: dict | None = None

    type: str | None = None
    owning_type: str | None = None
    covering_type: str | None = None
    paying_type: list[str] | None = None
    age: list[str] | None = None

    @field_validator('working_hours')
    @classmethod
    def working_hours_validator(cls, v: dict) -> dict:
        FacilityWorkingHours.model_validate(v)
        return v


class FilterItem(BaseModel):
    field: str
    eq: str | int
    gt: float
    lt: float


class FacilitySearchRequest(BaseModel):
    all: bool | None = None

    order_by: str | None = None
    order_desc: bool | None = None

    q: str | None = None
    x: float | None = None
    y: float | None = None

    limit: int | None = None
    offset: int | None = None

    hidden: bool | None = None

    filters: list[FilterItem] | None = None

    type: list[str] | None = None
    owning_type: list[str] | None = None
    covering_type: list[str] | None = None
    paying_type: list[str] | None = None
    age: list[str] | None = None


class FacilityPhoto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    url: str
    filename: str


class FacilityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID

    name: str
    owner: str
    address: str

    x: float | None = None
    y: float | None = None
    hidden: bool

    length: float | None = None
    width: float | None = None
    height: float | None = None
    depth: float | None = None
    area: float
    eps: int | None = None
    actual_workload: int | None = None
    annual_capacity: int | None = None

    accessibility: bool

    site: str | None = None
    phone_number: str | None = None
    document: str | int | None = None
    note: str | None = None

    working_hours: dict

    type: str
    owning_type: str | None = None
    covering_type: str | None = None
    paying_type: list[str]
    age: list[str]
    photo: list[FacilityPhoto]

    @field_validator('working_hours')
    @classmethod
    def working_hours_validator(cls, v: dict) -> dict:
        FacilityWorkingHours.model_validate(v)
        return v

    @staticmethod
    def from_service_model(f: FacilityServiceModel):
        facility = f.model_dump()
        facility['type'] = facility['type']['name']

        if facility['owning_type'] is not None:
            facility['owning_type'] = facility['owning_type']['name']

        if facility['covering_type'] is not None:
            facility['covering_type'] = facility['covering_type']['name']

        paying_type = []
        for fpt in facility['paying_type']:
            paying_type.append(fpt['name'])
        facility['paying_type'] = paying_type

        age = []
        for fpt in facility['age']:
            age.append(fpt['name'])
        facility['age'] = age
        return FacilityResponse.model_validate(facility)


class FacilitySearchResponse(BaseModel):
    count: int
    facilities: list[FacilityResponse]
