from datetime import datetime
from typing import List

from pydantic import BaseModel, validator


class OrderDetailsOut(BaseModel):
    product_id: str
    quantity: int

    @validator("quantity")
    def validate_quantity(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Quantity must be greater than 0.")
        return v


class OrderDetailsCollectionIn(BaseModel):
    items: List[OrderDetailsOut]


class OrderOut(BaseModel):
    id: int
    datetime: datetime

    class Config:
        orm_mode = True


class OrderCollectionOut(BaseModel):
    items: List[OrderOut]

    class Config:
        orm_mode = True


class OrderWithDetailsOut(OrderOut):
    items: List[OrderDetailsOut]

    class Config:
        orm_mode = True
