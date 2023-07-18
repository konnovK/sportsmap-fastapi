from pydantic import BaseModel, ConfigDict, EmailStr


class EmailPasswordRefreshServiceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    secret: str
    email: str


class EmailSubscriberRefreshServiceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    secret: str
    email: str
