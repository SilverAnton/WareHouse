import enum
from datetime import datetime
from typing import List
from sqlalchemy import Enum

from pydantic import BaseModel

from schemas.order_item import OrderItemCreate


class OrderStatus(str, enum.Enum):
    in_process = "in_process"
    shipped = "shipped"
    delivered = "delivered"


class OrderCreate(BaseModel):

    status: OrderStatus = OrderStatus.in_process
    order_items: List[OrderItemCreate]

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    created_at: datetime
    status: OrderStatus
    order_items: List[OrderItemCreate]

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    orders: List[OrderResponse]

    class Config:
        from_attributes = True


class OrderUpdate(BaseModel):
    status: OrderStatus | None = None
    order_items: List[OrderItemCreate] | None = None

    class Config:
        from_attributes = True


class OrderDelete(BaseModel):
    id: int

    class Config:
        from_attributes = True
