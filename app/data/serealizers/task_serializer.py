from pydantic import BaseModel


class TaskBase(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    user_id: int

    class Config:
        orm_mode = True


class TaskUpdateRequestSerializer(BaseModel):
    id: int
    title: str | None
    description: str | None
    status: str | None


class TaskListResponseSerializer(BaseModel):
    tasks: list[TaskBase]

    class Config:
        orm_mode = True


class TaskStatusRequestSerializer(BaseModel):
    status: str
    user_id: int | None


class SingleTaskRequestSerializer(BaseModel):
    id: int
