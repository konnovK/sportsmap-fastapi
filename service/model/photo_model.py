import uuid

from pydantic import BaseModel, ConfigDict


class PhotoServiceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    url: str
    filename: str
