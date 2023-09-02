from pydantic import BaseModel


class InventoryBase(BaseModel):
    name: str
    quantity: int
    price: float


class InventoryCreate(InventoryBase):
    pass


class InventorySchema(InventoryBase):
    id: int
