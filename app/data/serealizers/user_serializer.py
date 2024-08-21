from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    username: str
    password: str

    class Config:
        orm_mode = True


class UserCreateRequestSerializer(BaseModel):
    first_name: str
    last_name: str | None
    username: str
    password: str


class UserAuthRequestSerializer(BaseModel):
    username: str
    password: str


class UserCheckRequestSerializer(BaseModel):
    username: str
