from fastapi import FastAPI

from app.api.v1.tasks_router import tasks_router
from app.api.v1.users_router import user_router
from app.api.v1.auth_router import auth_router

app = FastAPI()
app.include_router(tasks_router)
app.include_router(user_router)
app.include_router(auth_router)
