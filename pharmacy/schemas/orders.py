from pydantic import BaseModel

from pharmacy.enums import OrderStatus
from pharmacy.schemas.users import UserSchema


class OrderItem(BaseModel):
    sub_total: float
    name: str
    quantity: int


class OrderSchema(BaseModel):
    id: int
    user: UserSchema | None = None
    status: OrderStatus
    total: float = 0
    order_items: list[OrderItem] = []
