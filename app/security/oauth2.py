from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr


fake_users_db = {
	"mascot": {
		"username": "mascot",
		"full_name": "Richard Fordjour",
		"email": "abudusamed@gmail.com",
		"hashed_password": "fakehashedsecret",
		"disabled": False
	}
}

app = FastAPI()

def  fake_hash_password(password: str):
	return "fakehashed" + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
	username: str
	email: EmailStr | None = None
	full_name: str | None = None
	disabled: bool | None = None


class UserInDB(User):
	hashed_password: str


def get_user(db, username: str):
	if username in db:
		user_dict = db[username]
		return UserInDB(**user_dict)