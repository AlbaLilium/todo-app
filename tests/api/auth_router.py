from fastapi import FastAPI, Security

from app.controllers.utils import oauth2_scheme
from tests.test_main import api_client

app = FastAPI()


@app.get("/tasks/")
def read_tasks(token: str = Security(oauth2_scheme)):
    if token is None:
        return {"msg": "Create an account first"}
    return {"token": token}


def test_sign_up(api_client):
    response = api_client.post("/user/auth/sign-up", json={
        "first_name": "string",
        "last_name": "string",
        "username": "string",
        "password": "string"
    })
    assert response.status_code == 201
