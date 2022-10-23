import sys

sys.path.append('../src/')
from entities import db_test, define_entities
from main import app, get_db

from fastapi.testclient import TestClient
from fastapi import *
from pony.orm import *
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def define_database_test():
    db = Database(**db_test)
    define_entities(db)
    db.generate_mapping(create_tables=True)
    with db_session:
        db.User(username="angelescch",email="angelescch@gmail.com",password=pwd_context.hash("ssssSSS1"),avatar="avatar.img")
    return db

app.dependency_overrides[get_db] = define_database_test

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
