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

def test_leave_match_success():
    pass

def test_leave_match_not_valid_match():
    pass

def test_leave_match_not_valid_user():
    pass

def test_leave_match_not