from sqlalchemy import Column, Integer, String
from app.database import Base
from .validators import AuthHandler as auth_handler


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = auth_handler.get_password_hash(password)

    def check_password(self, password: str) -> bool:
        return auth_handler.verify_password(password, self.password)
