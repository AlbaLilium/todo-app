from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from app.controllers.queries.task_queries import TaskOperation
from app.controllers.utils import security, is_status_correct
from app.data.enum import TaskStatusEnum
from app.data.serealizers.task_serializer import (SingleTaskRequestSerializer,
                                                  TaskBase,
                                                  TaskListResponseSerializer,
                                                  TaskStatusRequestSerializer,
                                                  TaskUpdateRequestSerializer)
from app.data.serealizers.utils_serializer import Pagination

tasks_router = APIRouter(prefix="/task", tags=["Task"])


def get_pagination_params(
        page_number: int = Query(1, ge=0), page_size: int = Query(10, gt=0)
):
    return Pagination(page_number=page_number, page_size=page_size)


@tasks_router.get("/", response_model=TaskListResponseSerializer)
async def get_all_tasks(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        pagination: Pagination = Depends(get_pagination_params),
):
    async with TaskOperation() as db:
        tasks_list = await db.get_all_tasks(
            page_number=pagination.page_number, page_size=pagination.page_size
        )
    return tasks_list


@tasks_router.get("/{task_id}")
async def get_task(
        data: SingleTaskRequestSerializer,
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    async with TaskOperation() as db:
        tasks_list = await db.get_task(data)
    return tasks_list


@tasks_router.patch("/{task_id}", response_model=TaskBase)
async def update_task(
        task: TaskUpdateRequestSerializer,
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    if task.status and is_status_correct(task.status):
        async with TaskOperation() as db:
            updated_task = await db.update_task_by_field(task)
    return updated_task


@tasks_router.patch("/{task_id}")
async def complete_task(
        task: TaskStatusRequestSerializer,
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    task.status = TaskStatusEnum.completed.value
    return await update_task(task)


@tasks_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task: SingleTaskRequestSerializer,
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    async with TaskOperation() as db:
        response = await db.delete_task(task)
        return {"message": response}


@tasks_router.post("")
async def create_task(
        task: TaskBase,
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    if is_status_correct(status):
        async with TaskOperation() as db:
            new_task = await db.insert_task(task)
    return new_task


@tasks_router.get("")
async def filter_task_by_status(
        status: Annotated[str, Query(max_length=50)],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        pagination: Pagination = Depends(get_pagination_params),
        user_id: Annotated[int | None, Query(max_length=50, gt=0)] = None,
):
    filter_tasks = TaskStatusRequestSerializer(status=status, user_id=user_id)
    if is_status_correct(status):
        async with TaskOperation() as db:
            tasks_list = await db.filter_by_status(
                filter_tasks,
                page_size=pagination.page_size,
                page_number=pagination.page_number,
            )
    return tasks_list
