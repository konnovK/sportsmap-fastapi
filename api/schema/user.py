import uuid

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None


class UserPatchRequest(BaseModel):
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserRefreshTokenRequest(BaseModel):
    access_token: str
    refresh_token: str


class UserRefreshPassword(BaseModel):
    new_password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    admin: bool


class UserLoginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    admin: bool
    access_token: str
    refresh_token: str
    access_token_expires_in: int
