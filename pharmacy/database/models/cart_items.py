from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from pharmacy.database.core import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    inventory_id: Mapped[int] = mapped_column(
        ForeignKey("inventories.id"),
        nullable=False,
    )
