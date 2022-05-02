from pydantic import BaseModel

# TODO Change data type of email to use email_validator


class UserBase(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    pass


class Token(BaseModel):
    access_token: str
