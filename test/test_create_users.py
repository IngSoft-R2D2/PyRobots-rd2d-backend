from fastapi.testclient import TestClient
from fastapi import status

from src.main import app

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
    assert response1.json() == {
        "id": 2,
        "operation_result": "Succesfully created!",
        }


def test_create_user_existing_username():
    response1 = client.post("/users/",
    json={
        "username": "string",
        "email": "original@example.com",
        "avatar": "string",
        "password": "Hola1234"
        })
    assert response1.status_code == status.HTTP_409_CONFLICT
    assert response1.json() == {"detail": "A user with this username already exists"}


def test_create_user_existing_email():
    response1 = client.post("/users/",
    json={
        "username": "original",
        "email": "user@example.com",
        "password": "Chau1234"
        })
    assert response1.status_code == status.HTTP_409_CONFLICT
    assert response1.json() == {"detail": "A user with this email already exists"}
