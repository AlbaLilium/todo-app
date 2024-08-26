from pydantic import BaseModel


class UserBase(BaseModel):
    """
    Base Serializer for User.

     ...

     Attributes
     ----------
      id: int
      first_name: str
      last_name: str | None
      username: str

     Notes
     ------
      ORM reading is supported
    """

    id: int
    first_name: str
    last_name: str | None
    username: str

    class Config:
        orm_mode = True


class UserCreateRequestSerializer(BaseModel):
    """
    User serializer for registration requests.

     ...

     Attributes
     ----------
      first_name: str
      last_name: str | None
      username: str
      password: str

    """

    first_name: str
    last_name: str | None
    username: str
    password: str


class UserAuthRequestSerializer(BaseModel):
    """
    User serializer for authentication requests.

     ...

     Attributes
     ----------
     username: str
     password: str

    """

    username: str
    password: str


class UserCheckRequestSerializer(BaseModel):
    """
    User serializer for registration requests.

     ...

     Attributes
     ----------
      username: str

    """
    username: str


class UserGetRequestSerializer(BaseModel):
    """
    User serializer for getting user's tasks requests.

     ...

    Attributes
    ----------
     id: int

    """

    id: int
