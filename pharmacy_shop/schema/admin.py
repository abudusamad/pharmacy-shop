from pydantic import BaseModel, EmailStr


class AdminBase(BaseModel):
    username: str
    email: EmailStr


class AdminCreate(AdminBase):
    password: str


class AdminSchema(AdminBase):
    id: int
