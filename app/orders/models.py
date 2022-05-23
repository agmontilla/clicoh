from datetime import datetime

import requests
from app.constants import USD_API_URL
from app.database import Base
from app.exceptions import USDRateNotFound
from app.products.models import Product
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False, default=datetime.now())
    order_details = relationship("OrderDetails", back_populates="order")

    def get_total(self) -> float:
        return sum(
            item.quantity * item.product_order_details.price
            for item in self.order_details
        )

    def get_total_usd(self) -> float:
        return self.get_total() / self.get_usd_rate()

    # TODO: Hardcode Value
    @staticmethod
    def get_usd_rate(mode: str = "Dolar Blue") -> float:
        """
        Gets the USD rate.
        """
        response = requests.get(USD_API_URL)
        response.raise_for_status()
        data = response.json()

        rate: float = 0

        for item in data:
            if item["casa"]["nombre"] == mode:
                rate = float(str.replace(item["casa"]["venta"], ",", "."))
                break
        else:
            raise USDRateNotFound(mode)

        return rate


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
