from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.controllers.queries.task_queries import TaskOperation
from app.controllers.utils import security
from app.data.serealizers.task_serializer import TaskListResponseSerializer
from app.data.serealizers.user_serializer import UserGetRequestSerializer
from app.data.serealizers.utils_serializer import Pagination

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.get(
    "/{user_id}/tasks", response_model=TaskListResponseSerializer, tags=["User"]
)
async def get_user_tasks(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        data: UserGetRequestSerializer,
        pagination: Pagination,
):
    async with TaskOperation() as db:
        tasks_list = await db.get_users_tasks(
            data, page_size=pagination.page_size, page_number=pagination.page_number)
        return tasks_list
