import pytest
from app.data.serealizers.user_serializer import UserCreateRequestSerializer, UserAuthRequestSerializer
from tests.test_main import api_client


@pytest.mark.anyio
def test_sign_up(api_client):
    user = {'first_name': 'John', 'last_name': 'Doe', 'username': 'testuser', 'password': 'password123'}
    response = api_client.post("/user/auth/sign-up", json=user,
                               headers={'accept': 'application/json', 'Content-Type': 'application/json'})
    assert response.status_code == 201, response.text
    assert "access_token" in response.json()
    assert "token_type" in response.json()

    user = UserCreateRequestSerializer(
        username="testuser2",
        password="pass"
    )
    response = api_client.post("/user/auth/sign-up", json=user.model_dump_json())
    assert response.status_code == 400, response.text
    assert response.json()["detail"] == "Password should be 6 or more symbols"


@pytest.mark.anyio
def test_sign_in(api_client):
    user = UserAuthRequestSerializer(
        username="testuser",
        password="password123"
    )
    response = api_client.post("/user/auth/sign-in", data=user.model_dump_json())
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()

    user = UserAuthRequestSerializer(
        username="invaliduser",
        password="invalidpassword"
    )
    response = api_client.post("/user/auth/sign-in", data=user.model_dump_json())
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
