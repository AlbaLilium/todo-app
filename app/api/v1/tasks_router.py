from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from app.controllers.queries.task_queries import TaskOperation
from app.controllers.utils import is_status_correct, security
from app.data.enum import TaskStatusEnum
from app.data.serealizers.task_serializer import (CreateTaskSerializer,
                                                  SingleTaskRequestSerializer,
                                                  TaskBase,
                                                  TaskListResponseSerializer,
                                                  TaskStatusRequestSerializer,
                                                  TaskUpdateRequestSerializer)
from app.data.serealizers.utils_serializer import Pagination

tasks_router = APIRouter(prefix="/tasks", tags=["Task"])


def get_pagination_params(
    page_number: int = Query(1, ge=0), page_size: int = Query(10, gt=0)
):
    return Pagination(page_number=page_number, page_size=page_size)


@tasks_router.get("/", response_model=TaskListResponseSerializer)
async def get_all_tasks(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    pagination: Pagination = Depends(get_pagination_params),
):
    """
    Get all tasks in database.

    Parameters
    ----------
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
    pagination: Pagination

    Returns
    -------
    task_list: TaskListResponseSerializer
    """
    async with TaskOperation() as db:
        tasks_list = await db.get_all_tasks(
            page_number=pagination.page_number, page_size=pagination.page_size
        )
    return tasks_list


@tasks_router.get("/{task_id}", response_model=TaskBase)
async def get_task(
    task_id: Annotated[int, Path(gt=0)],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
):
    """
    Get a task by id.
    Parameters
    ----------
    task_id: int
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]

    Returns
    -------
    task: TaskBase
    """
    async with TaskOperation() as db:
        task = await db.get_task(task_id)
    return task


@tasks_router.patch("/update/{task_id}", response_model=TaskBase)
async def update_task(
    task: TaskUpdateRequestSerializer,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    """
    Update task by one of fields: title, description, status.
    Parameters
    ----------
    task: TaskUpdateRequestSerializer
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]

    Returns
    -------
    updated_task:  TaskBase
    """
    if task.status and is_status_correct(task.status):
        async with TaskOperation() as db:
            updated_task = await db.update_task_by_field(task)
    return updated_task


@tasks_router.patch("/complete/{task_id}")
async def complete_task(
    task_id: Annotated[int, Path(gt=0)],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    status: str = TaskStatusEnum.completed.value,
):
    task = TaskUpdateRequestSerializer(
        id=task_id, status=status, description=None, title=None
    )
    return await update_task(task=task, credentials=credentials)


@tasks_router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task: SingleTaskRequestSerializer,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    """
    Delete task by id.

    Parameters
    ----------
    task: SingleTaskRequestSerialize
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]

    Returns
    -------
    response: dict[str:str]
    """
    async with TaskOperation() as db:
        response = await db.delete_task(task)
        return {"message": response}


@tasks_router.post(
    "/create/{task_id}",
)
async def create_task(
    task: CreateTaskSerializer,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    """

    Parameters
    ----------
    task: CreateTaskSerializer
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]

    Returns
    -------
    task_id: dict[str: str]

    """
    if is_status_correct(task.status):
        async with TaskOperation() as db:
            new_task_id = await db.insert_task(task)
        return {"id": str(new_task_id)}


@tasks_router.get("/filter/{task_id}")
async def filter_task_by_status(
    status: Annotated[str, Query(max_length=50)],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    pagination: Pagination = Depends(get_pagination_params),
    user_id: Annotated[int | None, Path(gt=0)] = None,
):
    """

    Parameters
    ----------
    status: Annotated[str, Query(max_length=50)],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    pagination: Pagination = Depends(get_pagination_params),
    user_id: Annotated[int | None, Path(gt=0)] = None,

    Returns
    -------
    task_list: TaskListResponseSerializer
    """
    filter_tasks = TaskStatusRequestSerializer(status=status, user_id=user_id)
    if is_status_correct(status):
        async with TaskOperation() as db:
            tasks_list = await db.filter_by_status(
                filter_tasks,
                page_size=pagination.page_size,
                page_number=pagination.page_number,
            )
    return tasks_list
