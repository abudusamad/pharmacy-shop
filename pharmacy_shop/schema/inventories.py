from datetime import date

from pydantic import BaseModel


class InventoryBase(BaseModel):
    manufacturer: str
    product_name: str
    description: str
    quantity: int
    price: float
    produced_date: date
    expiry_date: date


class InventoryCreate(InventoryBase):
    pass


class InventorySchema(InventoryBase):
    id: int
