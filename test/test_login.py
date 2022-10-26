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


def test_login_user_unauthorized_no_existing_username():
    response = client.post("/login/",
    data={
        "username": "angelescchh",
        "password": "ssssSSS1"
        })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == "This username does not exist"


def test_login_user_unauthorized_wrong_password():
    response = client.post("/login/",
    data={
        "username": "angelescch",
        "password": "ssssSSS11"
        })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == "Incorrect username or password"

def test_login_user_unauthorized_wrong_username():
    response = client.post("/login/",
    data={
        "username": "keyword",
        "password": "ssssSSS1"
        })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == "Incorrect username or password"

def test_login_user_unauthorized_not_confirmed_user():
    response = client.post("/login/",
    data={
        "username": "fake",
        "password": "8924F35bi"
        })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == "The user is not confirmed"