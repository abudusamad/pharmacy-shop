from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

fake_user_db= {
    "mascot":{
        "username": "mascotford",
        "full_name": "mascot ford",
        "email":"abudusamed@gmail.com",
        "hashed_password": "fakemascot",
        "disabled": False,
    },
       "richard":{
        "username": "rich",
        "full_name": "Richard Oppong",
        "email":"richoppong@gmail.com",
        "hashed_password": "fakerich",
        "disabled": True,
    },   
    
}

app = FastAPI()

def fake_hash_password(password: str):
    return "fakehashed" + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "token")

class User(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    disabled: bool | None =  None


class UserInDB(User):
    hashed_password: str
    
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
    
def fake_decode_token(token):
    user = get_user(fake_user_db, token)
    return user

async def get_currrent_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_currrent_user)]
):
    if current_user.disabled:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user
    
    
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_user_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code= 400,
            detail="Incorrect username or password"
        )
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, 
            detail="Incorrect username or password"
        )
    return { "access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_user_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user