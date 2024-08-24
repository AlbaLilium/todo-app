from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.controllers.utils import security, oauth2_scheme
from app.controllers.queries.task_queries import TaskOperation
from app.data.serealizers.task_serializer import TaskListResponseSerializer
from app.data.serealizers.user_serializer import UserGetRequestSerializer
from app.data.serealizers.utils_serializer import Pagination

user_router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@user_router.get('{user_id}/tasks', response_model=TaskListResponseSerializer, tags=["User"])
def get_user_tasks(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
                   data: UserGetRequestSerializer, pagination: Pagination):
    with (TaskOperation() as db):
        tasks_list = db.get_users_tasks(data, page_size=pagination.page_size, page_number=pagination.page_number)
    return tasks_list
