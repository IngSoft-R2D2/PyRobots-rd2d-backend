from pony.orm import *
from entities import *

from fastapi.testclient import TestClient
from fastapi import *

from main import app

import subprocess
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


client = TestClient(app)

access_token = ""
token_type = ""

user = {
	"username": "lucas",
    "email": "lucas@example.com",
	"avatar": "avatar_img",
	"password": "Lucas123"
}
fk_reg_robot = {
	'name': "MEGATRON",
	'avatar': "64base_coded_img",
	'behaviour_file': "64base_coded_file"
}
fk_reg_robot_no_avatar = {
	'name': "OPTIMUS PRIME1234",
	'behaviour_file': "64base_coded_file"
}
fk_reg_robot_inv_robot_name = {
	'name': "MEGATRON",
	'avatar': "64base_coded_img",
	'behaviour_file': "64base_coded_file"
}

with db_session:
    User(username=user["username"], password=pwd_context.hash(user["password"]),
             email=user["email"], avatar=user["avatar"])

def test_login_to_get_token():
	response = client.post(
		"/login/",
		data={"username": user["username"],
			"password": user["password"]}
	)
	assert response.status_code == status.HTTP_200_OK
	global access_token
	global token_type
	access_token = response.json()['access_token']
	token_type = response.json()['token_type']

def test_register_robot():
	response = client.post(
		"/robots/",
		json = {
            'name': "MEGATRON",
            'avatar': "64base_coded_img",
            'behaviour_file': "64base_coded_file"
        },
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
