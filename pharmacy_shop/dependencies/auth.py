from fastapi import  Depends, status
from fastapi.exceptions import  HTTPException
from jose import jwt, JWTError
 from typing import Annotated

from pharmacy_shop.dependencies.database import Database
from pharmacy_shop.dependencies.oauth_schemes import user_scheme
from pharmacy_shop.database.models.users import  User


def get_authenticated_user(db:Database, str = Depends(user_scheme))->:
    token_exception = HTTPException(
            status_code =status.HTTP_401_UNAUTHORIZED,
            detail = "invalid credentials"


    )


    try:
        data: dict[str, str] =jwt.decode(token=token, key ='something', algorithms =["HS256"])
    except JWTerror:

    user_id =int(data["sub"])
    user:User |None = db.get(User, user_id)
    if user is None:
        raise token_exception

    return user

AuthenticatedUser = Annotated[User, Depends(get_authenticated_user)]