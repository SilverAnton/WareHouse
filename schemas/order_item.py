from pydantic import BaseModel

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = 1  # Устанавливаем значение по умолчанию на 1

    class Config:
        from_attributes = True