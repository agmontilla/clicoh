from datetime import datetime
from typing import List

from pydantic import BaseModel, validator


class OrderIn(BaseModel):
    id: int
    datetime: datetime


class OrderDetails(BaseModel):
    product_id: str
    quantity: int

    @validator("quantity")
    def validate_quantity(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Quantity must be greater than 0.")
        return v


class OrderDetailsCollection(BaseModel):
    items: List[OrderDetails]


class OrderOut(BaseModel):
    id: int
    datetime: datetime

    class Config:
        orm_mode = True
