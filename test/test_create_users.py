import sys

sys.path.append('../src/')
 
from fastapi.testclient import TestClient
from fastapi import status

from main import app


client = TestClient(app)


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


def test_create_user_existing_username():
    response1 = client.post("/users/",
    json={
        "username": "lucas",
        "email": "raro@example.com",
        "avatar": "string",
        "password": "Hola1234"
        })
    assert response1.status_code == status.HTTP_409_CONFLICT
    assert response1.json() == {"detail": "A user with this username already exists"}


def test_create_user_existing_email():
    response1 = client.post("/users/",
    json={
        "username": "raro",
        "email": "lucas@example.com",
        "password": "Chau1234"
        })
    assert response1.status_code == status.HTTP_409_CONFLICT
    assert response1.json() == {"detail": "A user with this email already exists"}


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