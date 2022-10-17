from fastapi.testclient import TestClient
from fastapi import status

from src.main import app

client = TestClient(app)


def test_login_user():
    response1 = client.post("/login/",
    data={
        "username": "lucas",
        "password": "26Hi0284"
        })
    assert response1.status_code == status.HTTP_200_OK
    assert response1.json()['token_type'] == "bearer"
