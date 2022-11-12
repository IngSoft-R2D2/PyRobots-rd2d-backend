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
        "/login",
        data={"username": "angelescch","password": "ssssSSS1"}
    )
    assert response.status_code == status.HTTP_200_OK
    global access_token
    global token_type
    access_token = response.json()['access_token']
    token_type = response.json()['token_type']

def test_register_robot():
    with open("files_for_testing/robotito.py", "rb") as f1:
        files = {"behaviour_file": f1}
        response = client.post(
            "/robots/?name=RATCHET&avatar=64base_coded_img",
            headers={"Authorization": token_type + " " + access_token},
            files=files
        )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["operation_result"] == "Successfully created."

def test_register_robot_no_avatar():
    with open("files_for_testing/rir.py", "rb") as f1:
        files = {"behaviour_file": f1}
        response = client.post(
            "/robots/?name=OPTIMUS_PRIME",
            headers={"Authorization": token_type + " " + access_token},
            files=files
        )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["operation_result"] == "Successfully created."

def test_register_robot_with_robot_name_in_user_robots():
    with open("files_for_testing/roboto.py", "rb") as f1:
        files = {"behaviour_file": f1}
        response = client.post(
            "/robots/?name=MEGATRON&avatar=coded_img",
            headers={"Authorization": token_type + " " + access_token},
            files=files
        )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "This user has a robot with this name already."
