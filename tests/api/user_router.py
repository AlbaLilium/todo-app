import pytest
from app.api.v1.tasks_router import *
from app.api.v1.users_router import user_router
from app.data.serealizers.user_serializer import UsersListResponseSerializer
from tests.test_main import api_client


@pytest.mark.asyncio
async def test_get_user_tasks(api_client):
    api_client.include_router(user_router)

    response = await api_client.get("/users/1/tasks", headers={"Authorization": "Bearer <valid_token>"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, TaskListResponseSerializer)

    response = await api_client.get("/users/0/tasks", headers={"Authorization": "Bearer <valid_token>"})
    assert response.status_code == 422

    response = await api_client.get("/users/1/tasks", headers={"Authorization": "Bearer <invalid_token>"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_all_users(api_client):
    api_client.include_router(user_router)

    response = await api_client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, UsersListResponseSerializer)
