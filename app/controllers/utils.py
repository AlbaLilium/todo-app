from fastapi import HTTPException
from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from app.data.enum import TaskStatusEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBearer()


def is_status_correct(status):
    if status not in [task_status_type.value for task_status_type in TaskStatusEnum]:
        raise HTTPException(status_code=400, detail="Incorrect task status")
    return True
