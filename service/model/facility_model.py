import uuid

from pydantic import BaseModel, ConfigDict

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


class FacilityCreateServiceModel(BaseModel):
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
    document: str | None = None
    note: str | None = None

    working_hours: dict = EMPTY_WORKING_HOURS

    type: str
    owning_type: str = 'другая'
    covering_type: str | None = None
    paying_type: list[str] = []
    age: list[str] = []


class FacilityPatchServiceModel(BaseModel):
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
    document: str | None = None
    note: str | None = None

    working_hours: dict | None = None

    type: str | None = None
    owning_type: str | None = None
    covering_type: str | None = None
    paying_type: list[str] | None = None
    age: list[str] | None = None


class FacilityPutServiceModel(FacilityCreateServiceModel):
    # целый объект, на который поменяется тот, что был раньше
    pass


class FacilityTypeServiceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str


class FacilityPhotoServiceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    url: str
    filename: str


class FacilityServiceModel(BaseModel):
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
    document: str | None = None
    note: str | None = None

    working_hours: dict

    type: FacilityTypeServiceModel
    owning_type: FacilityTypeServiceModel | None = None
    covering_type: FacilityTypeServiceModel | None = None
    paying_type: list[FacilityTypeServiceModel]
    age: list[FacilityTypeServiceModel]
    photo: list[FacilityPhotoServiceModel]
