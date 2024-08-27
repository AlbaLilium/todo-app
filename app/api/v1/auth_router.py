from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (HTTPBearer, OAuth2PasswordBearer,
                              OAuth2PasswordRequestForm)

from app.api.depends import has_authenticated_user
from app.controllers.queries.user_queries import UserOperation
from app.controllers.token import login_for_access_token
from app.controllers.utils import oauth2_scheme, security
from app.data.serealizers.token_serializer import Token
from app.data.serealizers.user_serializer import (UserAuthRequestSerializer,
                                                  UserCheckRequestSerializer,
                                                  UserCreateRequestSerializer)

auth_router = APIRouter(prefix="/user/auth", tags=["Auth"])


@auth_router.post("/sign-up", status_code=status.HTTP_201_CREATED, response_model=Token)
async def sign_up(user: UserCreateRequestSerializer):
    if len(user.password) < 6:
        raise HTTPException(
            status_code=400, detail="Password should be 6 or more symbols"
        )
    async with UserOperation() as db:
        user_id = await db.insert_user(user)
    return login_for_access_token(user_id)


@auth_router.post("/sign-in", response_model=Token, tags=["Auth"])
async def sign_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = UserAuthRequestSerializer(
        username=form_data.username, password=form_data.password
    )
    is_checked_user = await has_authenticated_user(
        username=user.username, password=user.password
    )
    if not is_checked_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    async with UserOperation() as db:
        user = await db.get_user_by_username(
            UserCheckRequestSerializer(username=user.username)
        )

    return login_for_access_token(user.id)
