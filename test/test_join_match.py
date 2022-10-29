import sys
sys.path.append('../src/')
from main import app, get_db

from fastapi.testclient import TestClient
from fastapi import status

from database_for_testing import get_db_override
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


successfull_case_match_id = 10
error_case_not_valid_match_id = 50
error_case_user_in_match = 9
error_case_user_not_authenticated = 11

successfull_case_robot_id = 2
error_case_robot_id = 4


def test_join_match_success():
    response = client.put(
        "/matches/join/"+str(successfull_case_match_id)+"robot"+str(successfull_case_robot_id),
        headers={"Authorization": token_type + " " + access_token}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['operation_result'] == "Successfully joined."


def test_join_match_not_valid_match():
    response = client.put(
        "/matches/join/"+str(error_case_not_valid_match_id)+"robot"+str(successfull_case_robot_id),
        headers={"Authorization": token_type + " " + access_token}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail":"Match not found."}


def test_join_match_user_in_match_already():
    response = client.put(
        "/matches/join/"+str(error_case_user_in_match)+"robot"+str(successfull_case_robot_id),
        headers={"Authorization": token_type + " " + access_token}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail":"User is in match already."}


def test_join_match_not_authenticated_user():
    response = client.put(
        "/matches/join/"+str(error_case_user_not_authenticated)+"robot"+str(error_case_robot_id),
        headers={"Authorization": token_type + " " + wrong_token}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail":"Could not validate credentials"}