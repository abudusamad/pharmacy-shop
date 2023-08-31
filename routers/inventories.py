import sqlalchemy.exc
from sqlalchemy import select

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from pharmacy_shop.database.models.inventories import Inventory
from pharmacy_shop.schema.inventories import InventorySchema, InventoryCreate
from pharmacy_shop.dependencies.database import DatabaseConnection, get_inventory_or_404
from pharmacy_shop.dependencies.auth import  AuthenticatedUser


inventories = APIRouter()


@inventories.post("/inventories", response_model=InventorySchema, tags=["inventories"])
def create_inventory(
    inventory_data: InventoryCreate, database: DatabaseConnection
) -> Inventory:
    new_inventory = Inventory(**inventory_data.model_dump())

    try:
        database.add(new_inventory)
        database.commit()
        database.refresh(new_inventory)

        return new_inventory
    except sqlalchemy.exc.IntegrityError:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inventory might already exist",
        )


@inventories.get(
    "/inventories/", response_model=list[InventorySchema], tags=["inventories"]
)
def get_all_inventory(database: DatabaseConnection) -> list[Inventory]:
    try:
        db_inventories: list[Inventory | None] = database.scalars(
            select(Inventory)
        ).all()

        return db_inventories
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No inventories in the database.",
        )


@inventories.get(
    "/inventories/{inventory_id}", response_model=InventorySchema, tags=["inventories"]
)
def get_inventory_by_id(inventory_id: int, database: DatabaseConnection) -> Inventory:
    db_inventory: Inventory | None = get_inventory_or_404(
        inventory_id=inventory_id, database=database
    )
    return db_inventory


@inventories.delete(
    "/inventories/{inventory_id}", response_model=dict[str, str], tags=["inventories"]
)
def delete_inventory_id(inventory_id: int, database: DatabaseConnection):
    try:
        del_db_inventory: Inventory = get_inventory_or_404(
            inventory_id=inventory_id, database=database
        )

        database.delete(del_db_inventory)
        database.commit()
    except sqlalchemy.exc.InternalError:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inventory with id:{inventory_id} could not be deleted!",
        )
    return {"msg": "Inventory successfully deleted!"}
