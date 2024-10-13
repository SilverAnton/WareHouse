from sqlalchemy import ForeignKey, Integer, Column
from config.db import Base
from sqlalchemy.orm import relationship


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    quantity = Column(Integer, nullable=False, default=1)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

    def __str__(self):
        return f"Order Item ID: {self.id}"
