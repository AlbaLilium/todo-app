from fastapi import HTTPException
from sqlalchemy import select, or_

from app.controllers.queries.base_queries import BaseOperation
from app.data.models.user_model import User as UserModel
from app.data.serealizers.user_serializer import (UserBase,
                                                  UserCheckRequestSerializer,
                                                  UserCreateRequestSerializer,
                                                  UserGetRequestSerializer, UserAuthRequestSerializer)


class UserOperation(BaseOperation):
    async def insert_user(self, user: UserCreateRequestSerializer) -> UserBase:

        if await self.check_user(UserCheckRequestSerializer(username=user.username)):
            raise HTTPException(status_code=400, detail="User is already excited")

        user_obj = UserModel(
            first_name=user.first_name,
            username=user.username,
            password=user.password,
            last_name=user.last_name,
        )
        self.session.add(user_obj)

        return UserBase(
            id=user_obj.id,
            first_name=user_obj.first_name,
            username=user_obj.username,
            last_name=user_obj.last_name,
        )

    async def get_user(self, user: UserGetRequestSerializer | UserCheckRequestSerializer) -> UserBase:
        user = await self.session.execute(
            select(UserModel).where(
                or_(UserModel.id == user.id,
                    UserModel.username == user.username))
            )
        user = user.scalars().first()

        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        return UserBase(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            password=user.password,
        )

    async def check_user(self, user: UserCheckRequestSerializer | UserAuthRequestSerializer) -> bool | int:
        user = await self.session.execute(
            select(UserModel).where(UserModel.username == user.username))
        user = user.scalars().first()
        return True if user else False
