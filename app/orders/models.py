from datetime import datetime

from app.database import Base
from app.products.models import Product
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False, default=datetime.now())
    order_details = relationship("OrderDetails", back_populates="order")


class OrderDetails(Base):
    __tablename__ = "order_details"

    # id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    product_id = Column(
        String,
        ForeignKey(Product.id, ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    order = relationship("Order", back_populates="order_details")
    product_order_details = relationship("Product", back_populates="order_details")

    quantity = Column(Integer, default=1)
