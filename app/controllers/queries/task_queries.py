from fastapi import HTTPException
from sqlalchemy import or_
from app.data.models.task_model import Task as TaskModel
from app.controllers.queries.base_queries import BaseOperation
from app.data.serealizers.task_serializer import TaskBase, TaskListResponseSerializer, TaskUpdateRequestSerializer, \
    TaskDeleteRequestSerializer, TaskFilterRequestSerializer, TaskGetRequestSerializer


class TaskOperation(BaseOperation):
    def get_task_by_id(self, task: TaskGetRequestSerializer) -> TaskListResponseSerializer:

        query_obj_result = self.session.query(TaskModel).filter(
            or_(
                TaskModel.id == task.task_id,
                TaskModel.user_id == task.user_id
            )
        ).all()

        if not query_obj_result:
            raise HTTPException(status_code=400, detail="Object does not exist")

        return TaskListResponseSerializer(tasks=query_obj_result)

    def get_all_tasks(self) -> TaskListResponseSerializer:

        query_obj_result = self.session.query(TaskModel).all()
        return TaskListResponseSerializer(tasks=query_obj_result)

    def update_task_by_field(self, task: TaskUpdateRequestSerializer) -> TaskBase:

        task_obj = self.session.query(TaskModel).filter(TaskModel.id == task.task_id).all()

        if not task_obj:
            raise HTTPException(status_code=400, detail="Object does not exist")

        if task.title:
            task_obj.title = task.title
        elif task.status:
            task_obj.status = task.status
        elif task.description:
            task_obj.description = task.description

        self.session.add(task_obj)

        return TaskBase(title=task_obj.title,
                        description=task_obj.description,
                        status=task_obj.status,
                        user_id=task_obj.user_id)

    def insert_task(self, task: TaskBase) -> TaskBase:

        task_obj = TaskModel(title=task.title, status=task.status, user_id=task.user_id, description=task.description)
        self.session.add(task_obj)

        return TaskBase(title=task_obj.title,
                        description=task_obj.description,
                        status=task_obj.status,
                        user_id=task_obj.user_id)

    def delete_task(self, task: TaskDeleteRequestSerializer) -> str:

        task_obj = self.session.query(TaskModel).filter(TaskModel.id == task.task_id).all()

        if not task_obj:
            raise HTTPException(status_code=400, detail="Object does not exist")

        self.session.delete(task_obj)

        return "Object is deleted successfully"

    def filter_by_status(self, task: TaskFilterRequestSerializer) -> TaskListResponseSerializer:

        if task.user_id:
            query_obj_result = self.session.query(TaskModel).where(
                TaskModel.user_id == task.user_id,
                TaskModel.status == task.status,
            ).all()

        else:
            query_obj_result = self.session.query(TaskModel).where(TaskModel.status == task.status).all()

        return TaskListResponseSerializer(tasks=query_obj_result)
