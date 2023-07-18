from pydantic import BaseModel


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


class FacilityExcelItemServiceModel(BaseModel):
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
