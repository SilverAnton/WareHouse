from sqlalchemy import Integer, String, Text, Float, Column
from config.db import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True )
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    quantity_in_stock = Column(Integer, nullable=False)

    def __str__(self):
        return f"{self.name} ID: {self.id}"