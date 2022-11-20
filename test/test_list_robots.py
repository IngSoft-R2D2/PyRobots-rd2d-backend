import sys
from database_for_testing import get_db_override
sys.path.append('../src/')
from main import app, get_db

from fastapi.testclient import TestClient
from fastapi import status

app.dependency_overrides[get_db] = get_db_override

client = TestClient(app)

robots_list = {
    "5": {
        'name':"optimus",
        'avatar':"image1.64base_coded_img",
        'matches_played':0,
        'matches_won':0,
        'matches_lost':0,
        'matches_tied':0
    },
    "7": {
        'name':"ratchet",
        'avatar':"image2.64base_coded_img",
        'matches_played':0,
        'matches_won':0,
        'matches_lost':0,
        'matches_tied':0
    }
}

access_token = ""
token_type = ""
wrong_token = "eyJGOiJIUzIiIsInR5cCIkpXVCJyJzdisdWNhcyIsImV46MTY2ODDc2OH6ksb20clr.sg05kd.y-1k4Ul9hYApOgRTRnkgXpSTsm7PuuEvVx8UbBTJfbp7E4SEXQU"

def test_login_to_get_token():
    response = client.post(
        "/login",
        data={"username": "mati","password": "ssssSSSS1"}
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
    assert response.status_code==status.HTTP_200_OK
    assert response.json()==robots_list

def test_get_matches_not_autheticated_user():
    response = client.get(
        "/matches",
        headers={"Authorization": token_type + " " + wrong_token}   
    )
    assert response.status_code==status.HTTP_401_UNAUTHORIZED
    assert response.json()=={"detail":"Could not validate credentials"}