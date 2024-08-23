from fastapi import HTTPException

from app.controllers.queries.base_queries import BaseOperation
from app.data.models.user_model import User as UserModel
from app.data.serealizers.user_serializer import UserBase, UserCheckRequestSerializer, UserCreateRequestSerializer, \
    UserGetRequestSerializer


class UserOperation(BaseOperation):
    def insert_user(self, user: UserCreateRequestSerializer) -> UserBase:

        if self.check_user(UserCheckRequestSerializer(username=user.username)):
            raise HTTPException(status_code=400, detail="User is already excited")

        user_obj = UserModel(first_name=user.first_name, username=user.username, password=user.password,
                             last_name=user.last_name)
        self.session.add(user_obj)

        return UserBase(id=user_obj.id, first_name=user_obj.first_name, username=user_obj.username,
                        last_name=user_obj.last_name)

    def get_user(self, user: UserGetRequestSerializer) -> UserBase:
        user = self.session.query(UserModel).filter(UserModel.id == user.id).first()

        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        return UserBase(first_name=user.first_name, last_name=user.last_name, username=user.username,
                        password=user.password)

    def check_user(self, user: UserCheckRequestSerializer) -> bool:
        user = self.session.query(UserModel).filter(UserModel.username == user.username).first()

        return True if user else False
