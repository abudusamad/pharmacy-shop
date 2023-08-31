from pydantic import BaseModel


class TokenBearer(BaseModel):
    token_type: str = "bearer"
    token: str
