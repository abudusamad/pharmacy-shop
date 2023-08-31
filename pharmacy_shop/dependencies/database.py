from typing import Annotated
from sqlalchemy.orm import Session

from fastapi import HTTPException, status
from fastapi import Depends

from pharmacy_shop.database.core import session_maker
from pharmacy_shop.database.models.users import User
from pharmacy_shop.database.models.inventories import Inventory
from pharmacy_shop.database.models.admin import Admin


def get_database_connection() -> Session:
    with session_maker() as connection:
        yield connection


DatabaseConnection = Annotated[Session, Depends(get_database_connection)]


def get_user_or_404(user_id: int, database: DatabaseConnection) -> User:
    db_user: User | None = database.get(User, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{user_id} does not exist!",
        )
    return db_user


def get_inventory_or_404(inventory_id: int, database: DatabaseConnection) -> Inventory:
    db_inventory: Inventory | None = database.get(Inventory, inventory_id)

    if db_inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory with id:{inventory_id} does not exist!",
        )
    return db_inventory


def get_admin_or_404(admin_id: int, database: DatabaseConnection) -> Admin:
    db_admin: Admin | None = database.get(Admin, admin_id)

    if db_admin is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with id:{admin_id} does not exist!",
        )
    return db_admin
