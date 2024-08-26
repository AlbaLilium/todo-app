from typing import Annotated

from passlib.exc import UnknownHashError
from fastapi import Depends, HTTPException, status

from app.controllers.queries.user_queries import UserOperation
from app.controllers.token import verify_access_token, verify_password
from app.controllers.utils import oauth2_scheme
from app.data.serealizers.user_serializer import (UserBase,
                                                  UserGetRequestSerializer, UserAuthRequestSerializer)


async def has_authenticated_user(username: str, password: str) -> bool:
    async with UserOperation() as db:
        user = UserAuthRequestSerializer(username=username, password=password)
        is_user_existed = await db.check_user(user)
        if not is_user_existed:
            return False
        try:
            if not verify_password(password, user.password):
                return False
        except UnknownHashError:
            pass
        finally:
            return True


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserBase:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)

    async with UserOperation() as db:
        try:
            user = await db.get_user(UserGetRequestSerializer(username=token_data.username))
        except HTTPException(status_code=400, detail="User not found"):
            raise credentials_exception

    return user
