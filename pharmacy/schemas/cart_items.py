from pydantic import BaseModel


class CartItemBase(BaseModel):
    inventory_id: int
    quantity: int


class CartItemCreate(CartItemBase):
    pass


class CartItemSchema(CartItemBase):
    id: int
    user_id: int
