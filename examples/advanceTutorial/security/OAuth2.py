from datetime import timedelta, datetime

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

SECRET_KEY = "065b1937d2ee89648495749025096d65d4a1af64e03a3e933ef56f833824ab9a"
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db ={
	"mascot": {
		"username": "mascot",
		"full_name": "Richard Fordjour",
		"email": "abudusamed@gmail.com",
		"hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
		"disabled": False
	},
"abudu": {
		"username": "abudu",
		"full_name": "Abudu Samadu",
		"email": "abudusamed@gmail.com",
	    "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
		"disabled": True
	},

}


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
