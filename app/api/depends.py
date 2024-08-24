from typing import Annotated
from fastapi import HTTPException, Depends, status

from app.controllers.utils import security, oauth2_scheme
from app.controllers.queries.user_queries import UserOperation
from app.controllers.token import verify_access_token, verify_password
from app.data.serealizers.user_serializer import UserCheckRequestSerializer, UserBase, UserGetRequestSerializer


def has_authenticated_user(username: str, password: str) -> bool:
    with (UserOperation() as db):
        user = UserCheckRequestSerializer(username=username)
        is_user_existed = db.check_user(user)
        if not is_user_existed:
            return False
        if not verify_password(password, user.password):
            return False
        return True


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserBase:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)

    with (UserOperation() as db):
        try:
            user = db.get_user(UserGetRequestSerializer(username=token_data.username))
        except HTTPException(status_code=400, detail="User not found"):
            raise credentials_exception

    return user
