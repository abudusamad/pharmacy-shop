from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr




app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

class User(BaseModel):
    username: str
    email: str | None  = None
    full_name: str | None  = None
    disabled: bool | None = None
    
def fake_decode_token(token):
    return User(
        username= token + "mascot",
        email="abudusamad@hotmail.com",
        full_name="Abudu Samadu"
    )

async def get_currrent_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_currrent_user)]):
    return current_user

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}