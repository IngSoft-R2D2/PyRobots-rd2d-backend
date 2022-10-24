import sys
from database_for_testing import get_db_override
sys.path.append('../src/')
from main import app, get_db

from fastapi.testclient import TestClient
from fastapi import status

app.dependency_overrides[get_db] = get_db_override

client = TestClient(app)

access_token = ""
token_type = ""
wrong_token = "eyJGOiJIUzIiIsInR5cCIkpXVCJyJzdisdWNhcyIsImV46MTY2ODDc2OH6ksb20clr.sg05kd.y-1k4Ul9hYApOgRTRnkgXpSTsm7PuuEvVx8UbBTJfbp7E4SEXQU"

def test_login_to_get_token():
    response = client.post(
        "/login/",
        data={"username": "angelescch","password": "ssssSSS1"}
    )
    assert response.status_code == status.HTTP_200_OK
    global access_token
    global token_type
    access_token = response.json()['access_token']
    token_type = response.json()['token_type']

check = {
    'match_1': {'id': 1,
                'name': 'epic',
                'min_players': 2,
                'max_players': 4,
                'number_of_games': 100,
                'number_of_rounds': 10000,
                'password': 'secret',
                'is_finished': False,
                'creator': 1,
                'users': ['angelescch']},
    'match_2': {'id': 2,
                'name': 'pool',
                'min_players': 8,
                'max_players': 10,
                'number_of_games': 125,
                'number_of_rounds': 1010,
                'password': '',
                'is_finished': False,
                'creator': 2,
                'users': ['keyword']},
    'match_3': {'id': 3,
                'name': 'NGBI',
                'min_players': 3,
                'max_players': 5,
                'number_of_games': 5,
                'number_of_rounds': 10,
                'password': 'AGSV87NG4',
                'is_finished': False,
                'creator': 2,
                'users': ['keyword']},
    'match_4': {'id': 4,
                'name': 'KGN',
                'min_players': 3,
                'max_players': 5,
                'number_of_games': 5,
                'number_of_rounds': 10,
                'password': '',
                'is_finished': False,
                'creator': 1,
                'users': ['angelescch']}
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
    assert response.json() == check
