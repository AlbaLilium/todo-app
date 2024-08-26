from fastapi import HTTPException
from sqlalchemy import select, delete

from app.controllers.queries.base_queries import BaseOperation
from app.data.models.task_model import Task as TaskModel
from app.data.serealizers.task_serializer import (SingleTaskRequestSerializer,
                                                  TaskBase,
                                                  TaskListResponseSerializer,
                                                  TaskStatusRequestSerializer,
                                                  TaskUpdateRequestSerializer)
from app.data.serealizers.user_serializer import UserGetRequestSerializer


class TaskOperation(BaseOperation):
    async def get_task(self, task: SingleTaskRequestSerializer) -> TaskListResponseSerializer:

        query = await self.session.execute(
            select(TaskModel).where(TaskModel.id == task.task_id)
        )
        query_obj_result = query.scalars().all()
        if not query_obj_result:
            raise HTTPException(status_code=400, detail="Object does not exist")

        return TaskListResponseSerializer(tasks=query_obj_result)

    async def get_all_tasks(
            self, page_size: int, page_number: int
    ) -> TaskListResponseSerializer:

        query_obj_result = select(TaskModel)
        query_obj_result = self.paginate(query_obj_result, page_size, page_number)
        query_obj_result = await self.session.execute(query_obj_result)
        return TaskListResponseSerializer(tasks=query_obj_result.scalars().all())

    async def update_task_by_field(self, task: TaskUpdateRequestSerializer) -> TaskBase:

        task_obj = await self.session.execute(select(TaskModel).where(TaskModel.id == task.task_id))
        task_obj = task_obj.scalars().one()
        if not task_obj:
            raise HTTPException(status_code=400, detail="Object does not exist")

        if task.title:
            task_obj.title = task.title
        elif task.status:
            task_obj.status = task.status
        elif task.description:
            task_obj.description = task.description

        self.session.add(task_obj)

        return TaskBase(
            title=task_obj.title,
            description=task_obj.description,
            status=task_obj.status,
            user_id=task_obj.user_id,
        )

    async def insert_task(self, task: TaskBase) -> TaskBase:

        task_obj = TaskModel(
            title=task.title,
            status=task.status,
            user_id=task.user_id,
            description=task.description,
        )
        self.session.add(task_obj)

        return TaskBase(
            title=task_obj.title,
            description=task_obj.description,
            status=task_obj.status,
            user_id=task_obj.user_id,
        )

    async def delete_task(self, task: SingleTaskRequestSerializer) -> str:

        task_obj = await self.session.execute(
            delete(TaskModel).where(TaskModel.id == task.task_id)
        )
        task_obj = task_obj.scalars().all()
        if not task_obj:
            raise HTTPException(status_code=400, detail="Object does not exist")

        return "Object is deleted successfully"

    async def filter_by_status(
            self, task: TaskStatusRequestSerializer, page_size, page_number
    ) -> TaskListResponseSerializer:

        if task.user_id:
            query_obj_result = select(TaskModel).where(
                TaskModel.user_id == task.user_id,
                TaskModel.status == task.status,
            )

        else:
            query_obj_result = select(TaskModel).where(
                TaskModel.status == task.status
            )
        query_obj_result = self.paginate(
            query_obj_result, page_size=page_size, page_number=page_number
        )

        query_obj_result = await self.session.execute(query_obj_result)
        query_obj_result = query_obj_result.scalars().all()
        return TaskListResponseSerializer(tasks=query_obj_result)

    async def get_users_tasks(
            self, user: UserGetRequestSerializer, page_size: int, page_number: int
    ):
        query_obj_result = select(TaskModel).where(TaskModel.user_id == user.id)
        query_obj_result = self.paginate(query_obj_result, page_size, page_number)
        query_obj_result = await self.session.execute(query_obj_result)
        query_obj_result = query_obj_result.scalars().all()
        if not query_obj_result:
            raise HTTPException(status_code=400, detail="Object does not exist")

        return TaskListResponseSerializer(tasks=query_obj_result)
