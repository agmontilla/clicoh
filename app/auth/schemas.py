from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    pass

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
