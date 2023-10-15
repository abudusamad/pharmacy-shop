from fastapi import FastAPI
from fastapi.security import (
    OAuth2PasswordBearer,
)
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,

    },
    "abudu":{
        "username": "abudu",
        "full_name": "Abudu Samadu",
        "email": "abudusamadu@gmail.com",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
        "disabled": True,

    },
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str| None;
    scopes: list[str] = []


class User(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None  = None
    disabled: bool |None = None

class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme= OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user", "items":"Read items."}
)

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.hash(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def ger_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)