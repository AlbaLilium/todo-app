from fastapi import HTTPException
from app.data.models.user_model import User as UserModel
from app.controllers.queries.base_queries import BaseOperation
from app.data.serealizers.user_serializer import UserBase, UserCheckRequestSerializer, UserCreateRequestSerializer


class UserOperation(BaseOperation):
    def insert_user(self, user: UserCreateRequestSerializer) -> UserBase:
        self.check_user(UserCheckRequestSerializer(username=user.username),
                        error_400_detail="User is already existed")

        user_obj = UserModel(first_name=user.first_name, username=user.username, password=user.password,
                             last_name=user.last_name)
        self.session.add(user_obj)

        return UserBase(first_name=user.first_name, username=user.username, password=user.password,
                        last_name=user.last_name)

    def check_user(self, user: UserCheckRequestSerializer, error_400_detail: str = "User not found") -> UserBase:
        user = self.session.query(UserModel).filter(UserModel.username == user.username).first()

        if not user:
            raise HTTPException(400, error_400_detail)
        return UserBase(first_name=user.first_name, last_name=user.last_name, username=user.username,
                        password=user.password)
