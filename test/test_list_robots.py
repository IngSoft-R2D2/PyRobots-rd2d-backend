import sys
from database_for_testing import get_db_override
sys.path.append('../src/')
from main import app, get_db

from fastapi.testclient import TestClient
from fastapi import status

app.dependency_overrides[get_db] = get_db_override

client = TestClient(app)

fk_list_robots = {
    "1": "R2D2",
    "2": "MegaRobot",
    "3": "Robot3000",
    "4": "MEGATRON"
}

access_token = ""
token_type = ""
token_for_no_longer_user = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtdXllc3BlY2lhbCIsImV4cCI6MTY2NjYzMDI3OX0.fuMlzmMIv-uqTeCp31QP_ACf2lPZkxGy-C6JNlP8PCo"

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

def test_list_no_longer_existing_user():
    response = client.get(
        "/robots/",
        headers={"Authorization": token_type+" "+token_for_no_longer_user}
        )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == "Could not validate credentials"

def test_list_user_robots():
    response = client.get(
        "/robots/",
        headers={"Authorization": token_type+" "+access_token}
        )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == fk_list_robots
