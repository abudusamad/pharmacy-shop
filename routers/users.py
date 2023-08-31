import sqlalchemy.exc
from sqlalchemy import select
from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException

from pharmacy_shop.database.models.users import User
from pharmacy_shop.schema.token import TokenBearer
from pharmacy_shop.schema.users import UserSchema, UserCreate
from pharmacy_shop.dependencies.database import DatabaseConnection, get_user_or_404
from pharmacy_shop.dependencies.jwt import create_token, authenticate_user
from pharmacy_shop.security import Password

users = APIRouter()


@users.post("/users", response_model=UserSchema, tags=["users"])
def create_user(user_data: UserCreate, database: DatabaseConnection) -> User:
    user_data.password = Password.hash(user_data.password)
    new_user = User(**user_data.model_dump())

    try:
        database.add(new_user)
        database.commit()
        database.refresh(new_user)

        return new_user
    except sqlalchemy.exc.IntegrityError:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user might already exist",
        )

    @users.get("\current",response_model = [UserSechema])
    def get_current_user(user: AuthenticatedUser) -> User:
        return User


@users.post("/users/authenticate", response_model=TokenBearer)
def login_for_access_token(
    db: DatabaseConnection, credentials: OAuth2PasswordRequestForm = Depends()
):
    user: User | None = authenticate_user(db=db, credentials=credentials)

    data = {"sub": str(user.id)}
    token = create_token(data=data)

    bearer_token = TokenBearer(token=token)

    return bearer_token


@users.get("/users/", response_model=list[UserSchema], tags=["users"])
def get_all_users(database: DatabaseConnection) -> list[User]:
    try:
        db_users: list[User | None] = database.scalars(select(User)).all()

        return db_users
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users in the database.",
        )


@users.get("/{user_id}", response_model=UserSchema, tags=["users"])
def get_user_by_id(user_id: int, database: DatabaseConnection) -> User:
    db_user: User | None = get_user_or_404(user_id=user_id, database=database)
    return db_user


@users.delete("/{user_id}", response_model=dict[str, str], tags=["users"])
def delete_user_id(user_id: int, database: DatabaseConnection):
    try:
        del_db_user: User = get_user_or_404(user_id=user_id, database=database)

        database.delete(del_db_user)
        database.commit()
    except sqlalchemy.exc.InternalError:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"User with id:{user_id} could not be deleted!",
        )
    return {"msg": "Account successfully deleted!"}
