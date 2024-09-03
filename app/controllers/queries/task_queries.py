from fastapi import HTTPException
from sqlalchemy import delete, select

from app.controllers.queries.base_queries import BaseOperation
from app.data.models.task_model import Task as TaskModel
from app.data.serealizers.task_serializer import (CreateTaskSerializer,
                                                  SingleTaskRequestSerializer,
                                                  TaskBase,
                                                  TaskListResponseSerializer,
                                                  TaskStatusRequestSerializer,
                                                  TaskUpdateRequestSerializer)
from app.data.serealizers.user_serializer import UserGetRequestSerializer


class TaskOperation(BaseOperation):
    async def get_task(self, task_id: int) -> TaskBase:
        query = await self.session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        query_obj_result = query.scalars().first()
        if not query_obj_result:
            raise HTTPException(status_code=400, detail="Object does not exist")

        return TaskBase(
            id=query_obj_result.id,
            title=query_obj_result.title,
            description=query_obj_result.description,
            status=query_obj_result.status,
            user_id=query_obj_result.user_id,
        )

    async def get_all_tasks(
            self, page_size: int, page_number: int
    ) -> TaskListResponseSerializer:
        query_obj_result = self.paginate(select(TaskModel), page_size, page_number)
        query_obj_result = await self.session.execute(query_obj_result)
        query_obj_result = query_obj_result.scalars().all()
        return TaskListResponseSerializer(tasks=query_obj_result)

    async def update_task_by_field(self, task: TaskUpdateRequestSerializer) -> TaskBase:
        task_obj = await self.session.execute(
            select(TaskModel).where(TaskModel.id == task.id)
        )
        task_obj = task_obj.scalars().one()
        if not task_obj:
            raise HTTPException(status_code=400, detail="Object does not exist")

        if task.title:
            task_obj.title = task.title
        if task.status:
            task_obj.status = task.status
        if task.description:
            task_obj.description = task.description

        self.session.add(task_obj)
        self.session.commit()
        self.session.refresh(task_obj)

        return TaskBase(
            id=task.id,
            title=task_obj.title,
            description=task_obj.description,
            status=task_obj.status,
            user_id=task_obj.user_id,
        )

    async def insert_task(self, task: CreateTaskSerializer) -> int:
        task_obj = TaskModel(
            title=task.title,
            status=task.status,
            user_id=task.user_id,
            description=task.description,
        )
        self.session.add(task_obj)
        await self.session.commit()
        await self.session.refresh(task_obj)
        return task_obj.id

    async def delete_task(self, task: SingleTaskRequestSerializer) -> dict[str:str]:
        await self.session.execute(delete(TaskModel).where(TaskModel.id == task.id))
        return {"success": "task removed"}

    async def filter_by_status(
            self, task: TaskStatusRequestSerializer, page_size, page_number
    ) -> TaskListResponseSerializer:
        if task.user_id:
            query_obj_result = select(TaskModel).where(
                TaskModel.user_id == task.user_id,
                TaskModel.status == task.status,
            )

        else:
            query_obj_result = select(TaskModel).where(TaskModel.status == task.status)
        query_obj_result = self.paginate(
            query_obj_result, page_size=page_size, page_number=page_number
        )

        query_obj_result = await self.session.execute(query_obj_result)
        query_obj_result = query_obj_result.scalars().all()
        return TaskListResponseSerializer(tasks=query_obj_result)

    async def get_users_tasks(self, user_id: int, page_size: int, page_number: int):
        query_obj_result = select(TaskModel).where(TaskModel.user_id == user_id)
        query_obj_result = self.paginate(query_obj_result, page_size, page_number)
        query_obj_result = await self.session.execute(query_obj_result)
        query_obj_result = query_obj_result.scalars().all()
        if not query_obj_result:
            raise HTTPException(status_code=400, detail="Object does not exist")

        return TaskListResponseSerializer(tasks=query_obj_result)

    async def check_task_owner(self, user_id: int, task_id:int)->bool:
        task = await self.get_task(task_id=task_id)
        return True if task.user_id == user_id else False