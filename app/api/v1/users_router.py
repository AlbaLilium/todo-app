from collections import UserList
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from fastapi.security import HTTPAuthorizationCredentials

from app.api.v1.tasks_router import get_pagination_params
from app.controllers.queries.task_queries import TaskOperation
from app.controllers.queries.user_queries import UserOperation
from app.controllers.utils import security
from app.data.serealizers.task_serializer import TaskListResponseSerializer
from app.data.serealizers.user_serializer import (UserGetRequestSerializer,
                                                  UsersListResponseSerializer)
from app.data.serealizers.utils_serializer import Pagination

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get(
    "/{user_id}/tasks", response_model=TaskListResponseSerializer, tags=["User"]
)
async def get_user_tasks(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[int, Path(gt=0)],
    pagination: Pagination = Depends(get_pagination_params),
):
    async with TaskOperation() as db:
        tasks_list = await db.get_users_tasks(
            user_id, page_size=pagination.page_size, page_number=pagination.page_number
        )
        return tasks_list


# @user_router.get("/", tags=["User"], response_model=UsersListResponseSerializer)
# async def get_all_users():
#     async with UserOperation() as db:
#         return await db.get_users()
