import datetime
import uuid

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreateServiceModel(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None


class UserUpdateServiceModel(BaseModel):
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserServiceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    admin: bool
    active: bool
    created_at: datetime.datetime
