from fastapi.testclient import TestClient
from fastapi import status

from main import app

client = TestClient(app)


def test_login_user():
    response = client.post("/login/",
    data={
        "username": "lucas",
        "password": "26Hi0284"
        })
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['token_type'] == "bearer"

def test_login_user_unauthorized():
    response = client.post("/login/",
    data={
        "username": "jose",
        "password": "2B6y0284e"
        })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == "Incorrect username or password"
