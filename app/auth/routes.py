from http import HTTPStatus
from typing import List, Optional

from app.auth.schemas import UserCreate, Token
from app.auth.validators import AuthHandler
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

auth_router = APIRouter()
auth_handler = AuthHandler()

users: List[UserCreate] = [
    UserCreate(
        email="montilla05alfonso", password=auth_handler.get_password_hash("123")
    )
]


@auth_router.post("/signup", response_model=str, status_code=HTTPStatus.CREATED)
def signup(user: UserCreate) -> str:
    if user.email in [u.email for u in users]:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="User already exists"
        )

    hashed_password = auth_handler.get_password_hash(user.password)
    users.append(UserCreate(email=user.email, password=hashed_password))

    return "User Created"


@auth_router.post(
    "/login",
    response_model=Token,
    status_code=HTTPStatus.CREATED,
    responses={
        HTTPStatus.UNAUTHORIZED.value: {
            "description": "Invalid username and/or credentials"
        }
    },
)
def login(user: UserCreate) -> Token:
    user_flag: Optional[UserCreate] = None

    for u in users:
        if u.email == user.email:
            user_flag = u
            break

    if user_flag is None or not auth_handler.verify_password(user.password, u.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid username and/or credentials",
        )

    return Token(access_token="Bearer " + auth_handler.encode_token(user_flag.dict()))
