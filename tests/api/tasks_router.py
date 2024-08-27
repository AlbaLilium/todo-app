import pytest
from app.api.v1.tasks_router import *
from app.api.v1.auth_router import sign_up
from app.data.serealizers.user_serializer import UserCreateRequestSerializer
from tests.test_main import api_client


@pytest.fixture()
def get_user():
    user = UserCreateRequestSerializer(first_name="John", last_name="Doe", username="johndoe", password="johndoe")
    return sign_up(user)


@pytest.mark.anyio
def test_get_all_tasks(api_client, get_user):
    response = api_client.get("/tasks/", headers={"Authorization": f"Bearer {get_user}"})
    assert response.status_code == 200
    assert "tasks" in response.json()
    assert isinstance(response.json()["tasks"], list)


@pytest.mark.anyio
def test_get_task(api_client):
    response = api_client.get("/tasks/1")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    assert "status" in response.json()


@pytest.mark.anyio
def test_update_task(api_client, get_user):
    data = {
        "title": "Updated Task",
        "description": "This is an updated task",
        "status": TaskStatusEnum.in_progress.value
    }
    response = api_client.patch("/tasks/update/1", json=data, headers={"Authorization": f"Bearer {get_user}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    assert response.json()["description"] == "This is an updated task"
    assert response.json()["status"] == TaskStatusEnum.in_progress.value


@pytest.mark.anyio
def test_complete_task(api_client):
    response = api_client.patch("/tasks/complete/1", json={})
    assert response.status_code == 200
    assert response.json()["status"] == TaskStatusEnum.completed.value


@pytest.mark.anyio
def test_delete_task(api_client):
    response = api_client.delete("/tasks/delete/1")
    assert response.status_code == 204


@pytest.mark.anyio
def test_create_task(api_client):
    data = {
        "title": "New Task",
        "description": "This is a new task",
        "status": TaskStatusEnum.new.value
    }
    response = api_client.post("/tasks/create/1", json=data)
    assert response.status_code == 200
    assert "id" in response.json()


@pytest.mark.anyio
def test_filter_tasks_by_status(api_client):
    response = api_client.get("/tasks/filter/1?status=todo")
    assert response.status_code == 200
    assert "tasks" in response.json()
    assert all(task["status"] == TaskStatusEnum.todo.value for task in response.json()["tasks"])
