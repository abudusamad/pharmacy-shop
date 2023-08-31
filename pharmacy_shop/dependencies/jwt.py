from datetime import timedelta, datetime, timezone
from typing import Any, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from jose import jwt

from sqlalchemy import select

from pharmacy_shop.security import Password
from pharmacy_shop.dependencies.database import DatabaseConnection
from pharmacy_shop.database.models.users import User
from pharmacy_shop.database.models.admin import Admin


def create_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    now = datetime.now(timezone.utc)

    if expires_delta is None:
        expires_at = now + timedelta(minutes=15)
    else:
        expires_at = now + expires_delta

    to_encode.update({"iat": now, "exp": expires_at})
    return jwt.encode(to_encode, algorithm="HS256", key="something")


def authenticate_user(db: DatabaseConnection, credentials: OAuth2PasswordRequestForm):
    user: User | None = db.scalar(
        select(User).where(User.username == credentials.username)
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username or Password",
        )

    if Password.verify(credentials.password, user.password) is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username or Password",
        )
        
    return user


def authenticate_admin(db: DatabaseConnection, credentials: OAuth2PasswordRequestForm):
    admin: Admin | None = db.scalar(
        select(Admin).where(Admin.username == credentials.username)
    )

    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username or Password",
        )

    if Password.verify(credentials.password, admin.password) is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username or Password",
        )

    return admin


UserAuthentication = Annotated[User, Depends(authenticate_user)]
AdminAuthentication = Annotated[Admin, Depends(authenticate_admin)]
