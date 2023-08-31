from datetime import date

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr | None
    contact: str
    address: str | None
    date_of_birth: date | None


class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):
    id: int
