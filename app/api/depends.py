from passlib.exc import UnknownHashError

from app.controllers.queries.user_queries import UserOperation
from app.controllers.token import  verify_password
from app.data.serealizers.user_serializer import (UserAuthRequestSerializer)


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

