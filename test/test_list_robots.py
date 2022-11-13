import sys
from database_for_testing import get_db_override
sys.path.append('../src/')
from main import app, get_db

from fastapi.testclient import TestClient
from fastapi import status

app.dependency_overrides[get_db] = get_db_override

client = TestClient(app)

fk_list_robots = {
    "1": {
        'name':"R2D2",
        'matches_played':0,
        'matches_won':0,
        'matches_lost':0,
        'matches_drawed':0
    },
    "2": {
        'name':"MEGATRON",
        'matches_played':0,
        'matches_won':0,
        'matches_lost':0,
        'matches_drawed':0
    },
    "3": {
        'name':"Robot3000",
        'matches_played':0,
        'matches_won':0,
        'matches_lost':0,
        'matches_drawed':0
    }
}

access_token = ""
token_type = ""

def test_login_to_get_token():
    response = client.post(
        "/login",
        data={"username": "angelescch","password": "ssssSSS1"}
    )
    assert response.status_code == status.HTTP_200_OK
    global access_token
    global token_type
    access_token = response.json()['access_token']
    token_type = response.json()['token_type']


def test_list_user_robots():
    response = client.get(
        "/robots",
        headers={"Authorization": token_type+" "+access_token}
        )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == fk_list_robots
