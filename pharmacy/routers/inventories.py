import sqlalchemy.exc
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from sqlalchemy import select

from pharmacy.database.models.inventories import Inventory
from pharmacy.dependencies.database import Database, AnnotatedInventory
from pharmacy.schemas.inventories import InventorySchema, InventoryCreate

router = APIRouter()


@router.post("/inventories", response_model=InventorySchema)
def create_inventory(inventory_data: InventoryCreate, db: Database):
    inventory = Inventory(**inventory_data.model_dump())

    try:
        db.add(inventory)
        db.commit()
        db.refresh(inventory)

        return inventory
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="inventory already exists",
        )


@router.get("/inventories", response_model=list[InventorySchema])
def get_list_of_inventories(db: Database):
    return db.scalars(select(Inventory)).all()


@router.get("/inventories/{inventory_id}", response_model=InventorySchema)
def get_inventory(inventory: AnnotatedInventory):
    return inventory


@router.delete("/inventories/{inventory_id}")
def delete_inventory(inventory: AnnotatedInventory, db: Database):
    db.delete(inventory)
    db.commit()
