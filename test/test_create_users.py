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



def test_create_user_existing_username():
    response = client.post("/users/",
    json={
        "username": "angelescch",
        "email": "mati@example.com",
        "avatar": "salu",
        "password": "26Hi0284"
        })
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()['detail'] == "A user with this username already exists"


def test_create_user():
    response1 = client.post("/users/",
    json={
        "username": "lucas",
        "email": "lucas@example.com",
        "avatar": "salu",
        "password": "26Hi0284"
        })
    assert response1.status_code == status.HTTP_201_CREATED
    assert response1.json()['operation_result'] == "Succesfully created!"


def test_create_user_no_avatar():
    response1 = client.post("/users/",
    json={
        "username": "pedro",
        "email": "pedro@example.com",
        "password": "2B6y0284e"
        })
    assert response1.status_code == status.HTTP_201_CREATED
    assert response1.json()['operation_result'] == "Succesfully created!"


def test_create_user_existing_email():
    response1 = client.post("/users/",
    json={
        "username": "raro",
        "email": "angelescch@gmail.com",
        "password": "Chau1234"
        })
    assert response1.status_code == status.HTTP_409_CONFLICT
    assert response1.json() == {"detail": "A user with this email already exists"}


def test_create_user_no_email_format():
    response1 = client.post("/users/",
    json={
        "username": "lucas",
        "email": "lucasexample.com",
        "avatar": "salu",
        "password": "26Hi0284"
        })
    assert response1.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response1.json()
    for i in data['detail']:
        assert i['msg'] == 'value is not a valid email address'


def test_create_user_invalid_password_less_than_8():
    response1 = client.post("/users/",
    json={
        "username": "pass",
        "email": "pass@example.com",
        "avatar": "string",
        "password": "1234"
        })
    assert response1.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response1.json() == {"detail": "Invalid password format"}

def test_create_user_invalid_password_no_uppercase():
    response1 = client.post("/users/",
    json={
        "username": "pass",
        "email": "pass@example.com",
        "avatar": "string",
        "password": "hola1234"
        })
    assert response1.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response1.json() == {"detail": "Invalid password format"}

def test_create_user_invalid_password_no_lowercase():
    response1 = client.post("/users/",
    json={
        "username": "pass",
        "email": "pass@example.com",
        "avatar": "string",
        "password": "HOLA1234"
        })
    assert response1.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response1.json() == {"detail": "Invalid password format"}


def test_create_user_invalid_password_no_digit():
    response1 = client.post("/users/",
    json={
        "username": "pass",
        "email": "pass@example.com",
        "avatar": "string",
        "password": "hOLAHola"
        })
    assert response1.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response1.json() == {"detail": "Invalid password format"}
