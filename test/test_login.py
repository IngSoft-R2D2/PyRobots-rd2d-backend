import sys
from database_for_testing import get_db_override
sys.path.append('../src/')
from main import app, get_db

from fastapi.testclient import TestClient
from fastapi import status

app.dependency_overrides[get_db] = get_db_override

client = TestClient(app)

def test_login_user():
    response = client.post("/login/",
    data={
        "username": "angelescch",
        "password": "ssssSSS1"
        })
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['token_type'] == "bearer"


def test_login_user_unauthorized_wrong_username():
    response = client.post("/login/",
    data={
        "username": "angelescchh",
        "password": "ssssSSS1"
        })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == "Incorrect username or password"


def test_login_user_unauthorized_wrong_password():
    response = client.post("/login/",
    data={
        "username": "angelescch",
        "password": "ssssSSS11"
        })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == "Incorrect username or password"


def test_login_user_unauthorized_unregistered_username():
    response = client.post("/login/",
    data={
        "username": "jose",
        "password": "2B6y0284e"
        })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == "Incorrect username or password"
