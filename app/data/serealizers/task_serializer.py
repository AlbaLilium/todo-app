from pydantic import BaseModel


class TaskBase(BaseModel):
    """
    Base Serializer for Task.

     ...

     Attributes
     ----------
      id : int
      title: str
      description: str | None
      status: str
      user_id: int

     Notes
     ------
      ORM reading is supported

    """

    id: int
    title: str
    description: str | None
    status: str
    user_id: int

    class Config:
        from_attributes = True


class CreateTaskSerializer(BaseModel):
    """
    Base Serializer for Task.

     ...

     Attributes
     ----------
      title: str
      description: str | None
      status: str
      user_id: int

    """

    title: str
    description: str | None
    status: str
    user_id: int


class TaskUpdateRequestSerializer(BaseModel):
    """
    Task serializer for updating requests.

     ...

     Attributes
     ----------
      id : int
      title: str
      description: str | None
      status: str

    """

    id: int
    title: str | None
    description: str | None
    status: str | None
    user_id: int


class TaskListResponseSerializer(BaseModel):
    """
    Base Serializer for Task.

     ...

     Attributes
     ----------
      tasks: list[TaskBase]

     Notes
     ------
      ORM reading is supported
      See TaskBase for more information.

    """

    tasks: list[TaskBase]

    class Config:
        from_attributes = True


class TaskStatusRequestSerializer(BaseModel):
    """
    Task Serializer for filtering status's request.

     ...

     Attributes
     ----------
      status: str
      user_id: int | None

    """

    status: str
    user_id: int | None


class SingleTaskRequestSerializer(BaseModel):
    """
    Task Serializer for GET and DELETE requests.

     ...

     Attributes
     ----------
      id : int

    """

    id: int

class DeleteTaskRequestSerializer(BaseModel):
    """
    Task Serializer for DELETE requests.

     ...

     Attributes
     ----------
      id : int
      user_id: int

    """

    id: int
    user_id: int
