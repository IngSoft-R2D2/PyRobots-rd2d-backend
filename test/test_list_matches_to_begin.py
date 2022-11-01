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
        'match_14': {'creator': 1,
                      'id': 14,
                      'is_finished': False,
                      'max_players': 10,
                      'min_players': 2,
                      'name': 'match_that_can_begin',
                      'number_of_games': 125,
                      'number_of_rounds': 1010,
                      'password': '',
                      'users_robots': {'angelescch': 'R2D2', 'keyword': 'MEGATRON'}}
}

def test_register_robot_no_header_authorization():
    response = client.get("/matches/begin")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated"


def test_get_matches():
    response = client.get(
        "/matches/begin",
        headers={"Authorization": token_type+" "+access_token}
        )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == check
