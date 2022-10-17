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

false = False

fk_new_match_test = {
    'match_1':{
    'creator': 1,
    'id': 1,
    'is_finished': False,
    "name": "nombrepartida",
    "max_players": 4,
    "min_players": 2,
    "number_of_games": 100,
    "number_of_rounds": 10000,
    "password": "cualquiercosa123",
    "users": []
    },
    'match_2':{
    'creator': 1,
    'id': 2,
    'is_finished': False,
    "name": "partidasincontraseña",
    "max_players": 4,
    "min_players": 2,
    "number_of_games": 100,
    "number_of_rounds": 10000,
    "password": "",
    "users":[]
    }
}


def test_get_matches_unauthorized_wrong_token():
    response = client.get(
        "/matches/",
        headers={"Authorization": token_type + " " + wrong_token}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Could not validate credentials"

def test_register_robot_no_header_authorization():
    response = client.get("/matches/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated"


def test_get_matches():
    response = client.get(
        "/matches/",
        headers={"Authorization": token_type+" "+access_token}
        )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == fk_new_match_test
