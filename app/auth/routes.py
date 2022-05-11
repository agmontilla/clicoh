from http import HTTPStatus

from app.auth import schemas
from app.auth.services import register_user, verify_email_exists
from app.auth.validators import AuthHandler as auth_handler
from app.database import get_db
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

auth_router = APIRouter()


@auth_router.post("/signup", response_model=str, status_code=HTTPStatus.CREATED)
def signup(payload: schemas.User, database: Session = Depends(get_db)) -> str:
    user = verify_email_exists(payload.email, database)

    if user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="User already exists"
        )

    register_user(payload, database)

    return "User Created"


@auth_router.post(
    "/login",
    response_model=schemas.Token,
    status_code=HTTPStatus.CREATED,
    responses={
        HTTPStatus.UNAUTHORIZED.value: {
            "description": "Invalid username and/or credentials"
        }
    },
)
def login(payload: schemas.User, database: Session = Depends(get_db)) -> schemas.Token:

    user = verify_email_exists(payload.email, database)

    if not user or not user.check_password(payload.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid username and/or credentials",
        )

    user_chema = schemas.User.from_orm(user)

    return schemas.Token(
        access_token="Bearer " + auth_handler.encode_token(user_chema.dict())
    )
