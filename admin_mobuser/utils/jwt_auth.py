from datetime import timedelta, datetime, timezone

import jwt
from typing import Annotated, Union
from admin_mobuser.config.config import SECRET_KEY, ALGORITHM
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from admin_mobuser.models.user_model import TokenData
from admin_mobuser.firebase_handler import FirestoreHandler

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class JWTManager:
    def __init__(self) -> None:
        self.handler = FirestoreHandler()

    def create_access_token(self, data: dict,
                            expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return {'access_token': encoded_jwt}

    async def decode_token(self, token:
                           Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("email")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except InvalidTokenError:
            raise credentials_exception
        user = self.get_user(self.handler, email=token_data.email)
        if user is None:
            raise credentials_exception
        return user

    def get_user(self, email=None):
        user = self.handler.fetch_data('tabUserss', email)
        return user[0] if user else None
