from fastapi import HTTPException
from sqlalchemy import or_, select

from app.controllers.queries.base_queries import BaseOperation
from app.data.models.user_model import User as UserModel
from app.data.serealizers.user_serializer import (UserAuthRequestSerializer,
                                                  UserBase,
                                                  UserCheckRequestSerializer,
                                                  UserCreateRequestSerializer,
                                                  UserGetRequestSerializer,
                                                  UsersListResponseSerializer)


class UserOperation(BaseOperation):
    async def insert_user(self, user: UserCreateRequestSerializer) -> int:

        if await self.check_user(UserCheckRequestSerializer(username=user.username)):
            raise HTTPException(status_code=400, detail="User is already excited")

        user_obj = UserModel(
            first_name=user.first_name,
            username=user.username,
            password=user.password,
            last_name=user.last_name,
        )
        self.session.add(user_obj)
        self.session.commit()
        self.session.refresh(user_obj)

        return user_obj.id

    async def get_user_by_id(
        self, user: UserGetRequestSerializer | UserCheckRequestSerializer
    ) -> UserBase:
        user = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id)
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

    async def get_user_by_username(self, user: UserCheckRequestSerializer) -> UserBase:
        user = await self.session.execute(
            select(UserModel).where(UserModel.username == user.username)
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

    async def check_user(
        self, user: UserCheckRequestSerializer | UserAuthRequestSerializer
    ) -> bool | int:
        user = await self.session.execute(
            select(UserModel).where(UserModel.username == user.username)
        )
        user = user.scalars().first()
        return True if user else False

    # async def get_users(self):
    #     users = await self.session.execute(select(UserModel))
    #     users = users.scalars().all()
    #     return UsersListResponseSerializer(users_list=users)
