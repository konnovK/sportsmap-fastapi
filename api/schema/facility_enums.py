from pydantic import BaseModel


class FacilityTypeResponse(BaseModel):
    data: list[str]
