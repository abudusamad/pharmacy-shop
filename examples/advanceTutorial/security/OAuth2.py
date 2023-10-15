from pydantic import BaseModel

SECRET_KEY  = "beaa624b7f6971c59e0efa8c743467ee4fd3b0ddfa5e59cd34da924306256c8f
"
ALGORITHM ="HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 30

fake_user_db = {
    "mascot":{
        "username": "mascot",
        "full_name": "Richard Fordjour",
        "email": "abudusamed@gmail.com",
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

