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


class TaskFilterRequestSerializer(BaseModel):
    status: str
    user_id: int | None


class TaskDeleteRequestSerializer(BaseModel):
    id: int


class TaskGetRequestSerializer(BaseModel):
    id: int | None
    user_id: int | None
