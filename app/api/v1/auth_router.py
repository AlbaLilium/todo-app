from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.controllers.utils import security, oauth2_scheme
from app.api.depends import has_authenticated_user
from app.controllers.queries.user_queries import UserOperation
from app.controllers.token import login_for_access_token
from app.data.serealizers.token_serializer import Token
from app.data.serealizers.user_serializer import UserCreateRequestSerializer, UserAuthRequestSerializer


auth_router = APIRouter(
    prefix="/user/auth",
    tags=["Auth"]
)

@auth_router.post("/sign-up", status_code=status.HTTP_201_CREATED, response_model=Token)
def sign_up(user: UserCreateRequestSerializer):
    with (UserOperation() as db):
        new_user = db.insert_user(user)
    user_authentication = UserAuthRequestSerializer(username=user.username, password=user.password)
    return login_for_access_token(user_authentication)


@auth_router.put("/sign-in", response_model=Token, tags=["Auth"])
def sign_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = UserAuthRequestSerializer(username=form_data.username, password=form_data.password)
    is_checked_user = has_authenticated_user(username=user.username, password=user.password)
    if not is_checked_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return login_for_access_token(user)
