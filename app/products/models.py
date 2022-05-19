from uuid import uuid4

from app.database import Base
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(String, default=lambda: uuid4().hex, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    order_details = relationship("OrderDetails", back_populates="product_order_details")
