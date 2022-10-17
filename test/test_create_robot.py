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


fk_reg_robot = {
    'name': "MEGATRON",
    'avatar': "64base_coded_img",
    'behaviour_file': "64base_coded_file"
}
fk_reg_robot_no_avatar = {
    'name': "OPTIMUS PRIME",
    'behaviour_file': "64base_coded_file"
}
fk_reg_robot_inv_robot_name = {
    'name': "MEGATRON",
    'avatar': "64base_coded_img",
    'behaviour_file': "64base_coded_file"
}


def test_register_robot_unauthorized_wrong_token():
    response = client.post(
        "/robots/",
        json = fk_reg_robot,
        headers={"Authorization": token_type + " " + wrong_token}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Could not validate credentials"


def test_register_robot_no_header_authorization():
    response = client.post(
        "/robots/",
        json = fk_reg_robot
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated"


def test_register_robot():
    response = client.post(
        "/robots/",
        json = fk_reg_robot,
        headers={"Authorization": token_type + " " + access_token}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["operation_result"] == "Successfully created."


def test_register_robot_no_avatar():
    response = client.post(
        "/robots/",
        json = fk_reg_robot_no_avatar,
        headers={"Authorization": token_type + " " + access_token}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["operation_result"] == "Successfully created."


def test_register_robot_with_robot_name_in_user_robots():
    response = client.post(
        "/robots/",
        json = fk_reg_robot_inv_robot_name,
        headers={"Authorization": token_type + " " + access_token}
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "This user has a robot with this name already."
