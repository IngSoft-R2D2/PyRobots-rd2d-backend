import sys

sys.path.append('../src/')
from entities import db_test, define_entities
from main import app, get_db

from fastapi.testclient import TestClient
from fastapi import *
from pony.orm import *
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def define_database_test():
    db = Database(**db_test)
    define_entities(db)
    db.generate_mapping(create_tables=True)
    with db_session:
        db.User(username="angelescch",email="angelescch@gmail.com",password=pwd_context.hash("ssssSSS1"),avatar="avatar.img")
        db.Robot(user = db.User.get(username="angelescch"), name="R2D2", avatar="image.jpg", behaviour_file="RSD2.py")
        db.Robot(user = db.User.get(username="angelescch"), name="MegaRobot", avatar="image.jpg", behaviour_file="MegaRobot.py")
        db.Robot(user = db.User.get(username="angelescch"), name="Robot3000", avatar="image.jpg", behaviour_file="Robot3000.py")
    return db

app.dependency_overrides[get_db] = define_database_test


client = TestClient(app)

fk_list_robots = {
    "1": "R2D2",
    "2": "MegaRobot",
    "3": "Robot3000"
}


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

def test_print():
    response = client.get(
        "/robots/",
        headers={"Authorization": token_type+" "+access_token}
        )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == fk_list_robots
