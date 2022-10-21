import sys

sys.path.append('../src/')

from fastapi.testclient import TestClient
from fastapi import *

from main import app


client = TestClient(app)

access_token = ""
token_type = ""
wrong_token = "eyJGOiJIUzIiIsInR5cCIkpXVCJyJzdisdWNhcyIsImV46MTY2ODDc2OH6ksb20clr.sg05kd.y-1k4Ul9hYApOgRTRnkgXpSTsm7PuuEvVx8UbBTJfbp7E4SEXQU"


def test_login_to_get_token():
    response = client.post(
        "/login/",
        data={"username": "lucas","password": "26Hi0284"}
    )
    assert response.status_code == status.HTTP_200_OK
    global access_token
    global token_type
    access_token = response.json()['access_token']
    token_type = response.json()['token_type']


fk_new_match = {
    "name": "nombrepartida",
    "max_players": 4,
    "min_players": 2,
    "number_of_games": 100,
    "number_of_rounds": 10000,
    "password": "cualquiercosa123"
}
fk_new_match_no_password = {
    "name": "partidasincontraseña",
    "max_players": 4,
    "min_players": 2,
    "number_of_games": 100,
    "number_of_rounds": 10000,
    "password": ""
}
fk_new_match_many_max_players = {
    "name": "partidallena",
    "max_players": 16,
    "min_players": 2,
    "number_of_games": 100,
    "number_of_rounds": 10000,
    "password": "cualquiercosa123"
}
fk_new_match_few_max_players = {
    "name": "partidallena",
    "max_players": 1,
    "min_players": 2,
    "number_of_games": 100,
    "number_of_rounds": 10000,
    "password": "cualquiercosa123"
}

fk_new_match_few_min_players = {
    "name": "otrapartida",
    "max_players": 3,
    "min_players": 0,
    "number_of_games": 100,
    "number_of_rounds": 10000,
    "password": "cualquiercosa123"
}
fk_new_match_many_games = {
    "name": "otrapartida",
    "max_players": 3,
    "min_players": 2,
    "number_of_games": 500,
    "number_of_rounds": 10000,
    "password": "cualquiercosa123"
}
fk_new_match_many_rounds = {
    "name": "otrapartida",
    "max_players": 3,
    "min_players": 2,
    "number_of_games": 100,
    "number_of_rounds": 10001,
    "password": "cualquiercosa123"
}
fk_new_match_few_games = {
    "name": "otrapartida",
    "max_players": 3,
    "min_players": 2,
    "number_of_games": 0,
    "number_of_rounds": 5000,
    "password": "cualquiercosa123"
}
fk_new_match_few_rounds = {
    "name": "otrapartida",
    "max_players": 3,
    "min_players": 2,
    "number_of_games": 50,
    "number_of_rounds": 0,
    "password": "cualquiercosa123"
}
fk_new_match_wrong_maxmin_relac = {
    "name": "otrapartida",
    "max_players": 8,
    "min_players": 10,
    "number_of_games": 50,
    "number_of_rounds": 0,
    "password": "cualquiercosa123"
}

def test_create_match_unauthorized_wrong_token():
    response = client.post(
        "/matches/",
        json = fk_new_match,
        headers={"Authorization": token_type + " " + wrong_token}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Could not validate credentials"


def test_create_match_no_header_authorization():
    response = client.post(
        "/matches/",
        json = fk_new_match
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated"


def test_create_match():
    response = client.post(
        "/matches/",
        json = fk_new_match,
        headers={"Authorization": token_type + " " + access_token}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["operation_result"] == "Successfully created."


def test_create_match_no_password():
    response = client.post(
        "/matches/",
        json = fk_new_match_no_password,
        headers={"Authorization": token_type + " " + access_token}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["operation_result"] == "Successfully created."


def test_create_match_with_many_max_players():
    response = client.post(
        "/matches/",
        json = fk_new_match_many_max_players,
        headers={"Authorization": token_type + " " + access_token}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Invalid maximum number of players."

def test_create_match_with_few_max_players():
    response = client.post(
        "/matches/",
        json = fk_new_match_few_max_players,
        headers={"Authorization": token_type + " " + access_token}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Invalid maximum number of players."


def test_create_match_with_few_min_players():
    response = client.post(
        "/matches/",
        json = fk_new_match_few_min_players,
        headers={"Authorization": token_type + " " + access_token}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Invalid minimum number of players."


def test_create_match_with_many_rounds():
    response = client.post(
        "/matches/",
        json = fk_new_match_many_rounds,
        headers={"Authorization": token_type + " " + access_token}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Invalid number of rounds."

def test_create_match_with_few_rounds():
    response = client.post(
        "/matches/",
        json = fk_new_match_few_rounds,
        headers={"Authorization": token_type + " " + access_token}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Invalid number of rounds."


def test_create_match_with_many_games():
    response = client.post(
        "/matches/",
        json = fk_new_match_many_games,
        headers={"Authorization": token_type + " " + access_token}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Invalid number of games."


def test_create_match_with_few_games():
    response = client.post(
        "/matches/",
        json = fk_new_match_few_games,
        headers={"Authorization": token_type + " " + access_token}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Invalid number of games."


def test_create_match_with_wrong_maxmin_relac():
    response = client.post(
        "/matches/",
        json = fk_new_match_wrong_maxmin_relac,
        headers={"Authorization": token_type + " " + access_token}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Minimum number of players must not be greater than the maximun number of players."
