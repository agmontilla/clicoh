from pydantic import BaseModel, validator
from typing import List


class ProductIn(BaseModel):
    name: str
    price: float
    stock: int

    @validator("price")
    def validate_price(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

    @validator("stock")
    def validate_stock(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Stock cannot be negative")
        return v

    class Config:
        orm_mode = True


class ProductOut(ProductIn):
    id: str


class ProductsOutCollection(BaseModel):
    items: List[ProductOut]
