from pydantic import BaseModel
from typing import List

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    quantity_in_stock: int

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    quantity_in_stock: int

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    products: List[ProductResponse]

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    quantity_in_stock: int | None = None

    class Config:
        from_attributes = True

class ProductDelete(BaseModel):
    id: int

    class Config:
        from_attributes = True