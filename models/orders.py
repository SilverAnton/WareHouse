import enum
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, Column, Enum, DateTime
from config.db import Base


class OrderStatus(enum.Enum):
    in_process = "in_process"
    shipped = "shipped"
    delivered = "delivered"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    status = Column(Enum(OrderStatus), default=OrderStatus.in_process, nullable=True)

    order_items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"Order ID: {self.id}"
