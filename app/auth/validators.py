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

    def get_password_hash(self, password: str) -> Union[Any, str]:
        return self.PWD_CONTEXT.hash(password)

    def verify_password(self, password: str, hashed: str) -> Union[Any, bool]:
        return self.PWD_CONTEXT.verify(password, hashed)

    def encode_token(self, user: Dict) -> Union[Any, str]:
        jwt_payload = {
            "exp": datetime.utcnow() + timedelta(minutes=5),
            "user": user,
        }
        return jwt.encode(jwt_payload, self.SECRET, algorithm=self.ALGORITHMS)

    def decode_token(self, token: str) -> Any:
        try:
            payload = jwt.decode(token, self.SECRET, algorithms=self.ALGORITHMS)
        except exceptions.JWEInvalidAuth:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token"
            )
        except exceptions.ExpiredSignatureError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Token expired"
            )

        return payload["user"]

    def get_current_user(
        self, auth: HTTPAuthorizationCredentials = Security(SECURITY)
    ) -> Any:
        return self.decode_token(auth.credentials)
