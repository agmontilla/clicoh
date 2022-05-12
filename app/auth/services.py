from typing import Any, Union
from app.auth import models, schemas
from sqlalchemy.orm import Session


def verify_email_exists(email: str, database: Session) -> Union[models.User, None, Any]:
    return database.query(models.User).filter(models.User.email == email).first()


def register_user(user: schemas.User, database: Session) -> models.User:
    new_user = models.User(**user.dict())
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user
