from pydantic import BaseModel, EmailStr


class EmailSuggestionsRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    text: str | None = None


class EmailOfferObjectRequest(BaseModel):
    owner: str
    address: str
    note: str | None = None


class EmailSubscribeRequest(BaseModel):
    email: EmailStr


class PasswordRefreshRequest(BaseModel):
    email: EmailStr
