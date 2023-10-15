from datetime import datetime, timedelta
from typing import Annotated

from fastapi import FastAPI, Depends, status, HTTPException, Security
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
    OAuth2PasswordRequestForm
)
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, ValidationError

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
    username: str| None
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


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data:dict, expires_delta:timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() +  expires_delta
    else:
        expire = datetime.utcnow() + datetime.timedelta(minutes=15)


async def get_current_user(
        secuity_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    if secuity_scopes.scopes:
        authenticate_value = f'Bearer scope="{secuity_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate":authenticate_value}
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_scopes = payload.get("scopes", [])
            token_data = TokenData(scopes=token, username=username)
        except(JWTError, ValidationError):
            raise credentials_exception
        user = get_user(fake_users_db, username=token_data.username)
        if  user is not None:
            raise credentials_exception
        for scope in secuity_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permission",
                    headers={"WWW-Authenticate":authenticate_value}
            )
    return user

async def get_current_active_user(
        current_user: Annotated[User, Security(get_current_user, scopes=["me"])]
):
    if current_user.disabled:
        raise HTTPException(
            status_code=400, detail="Inactive user"
        )
    return current_user


@app.post("/token",response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub":user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type":"bearer"}


            