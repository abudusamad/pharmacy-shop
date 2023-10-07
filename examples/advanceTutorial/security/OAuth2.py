from datetime import timedelta, datetime

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
	access_token: str
	token_type: str


class TokenData(BaseModel):
	username: str | None = None
	scopes: list[str] = []


class User(BaseModel):
	username: str
	email: EmailStr | None = None
	full_name: str | None = None
	disabled: bool | None = None


class UserInDB(User):
	hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
	tokenUrl="token",
	scopes={"me": "Read information about the current user.", "items": "Read items."}
)


app = FastAPI()


def verify_password(plain_password, hashed_password):
	return pwd_context.verify(plain_password, hashed_password)


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

def create_access_token(data: dict, expire_delta: timedelta | None = None):
	to_encode = data.copy()
	if expire_delta:
		expire = datetime.utcnow() + expire_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=15)
	to_encode.update({"exp": expire})
