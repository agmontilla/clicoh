from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Any, Dict, Union

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, exceptions
from passlib.context import CryptContext


class AuthHandler:

    SECURITY = HTTPBearer()
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET = "secret"
    ALGORITHMS = "HS256"

    @classmethod
    def get_password_hash(cls, password: str) -> Union[Any, str]:
        return cls.PWD_CONTEXT.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed: str) -> Union[Any, bool]:
        return cls.PWD_CONTEXT.verify(password, hashed)

    @classmethod
    def encode_token(cls, user: Dict) -> Union[Any, str]:
        jwt_payload = {
            "exp": datetime.utcnow() + timedelta(minutes=5),
            "user": user,
        }
        return jwt.encode(jwt_payload, cls.SECRET, algorithm=cls.ALGORITHMS)

    @classmethod
    def decode_token(cls, token: str) -> Any:
        try:
            payload = jwt.decode(token, cls.SECRET, algorithms=cls.ALGORITHMS)
        except exceptions.JWEInvalidAuth:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token"
            )
        except exceptions.ExpiredSignatureError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Token expired"
            )

        return payload["user"]

    @classmethod
    def get_current_user(
        cls, auth: HTTPAuthorizationCredentials = Security(SECURITY)
    ) -> Any:
        return cls.decode_token(auth.credentials)
