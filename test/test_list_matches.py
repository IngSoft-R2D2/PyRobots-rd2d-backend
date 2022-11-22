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
        data={"username": "mati","password": "ssssSSSS1"}
    )
    assert response.status_code == status.HTTP_200_OK
    global access_token
    global token_type
    access_token = response.json()['access_token']
    token_type = response.json()['token_type']


matches_list = {
  "match_1": {
    "id": 1,
    "name": "partida1",
    "min_players": 2,
    "max_players": 4,
    "number_of_games": 123,
    "number_of_rounds": 123,
    "is_secured": False,
    "is_started": False,
    "is_finished": False,
    "creator": 4,
    'creator_name': 'mati',
    "user_id": 4,
    "user_name": "mati",
    "players": {
      "mati": {
        "robot_id": "5",
        "robot_name": "optimus"
      },
      "juan": {
        "robot_id": "6",
        "robot_name": "megatron"
      },
      "angelescch": {
        "robot_id": "1",
        "robot_name": "R2D2"
      }
    },
    'results': {},
    "user_is_creator": True,
    "is_available_to_join": False,
    "is_available_to_leave": False,
    "is_ready_to_start": True,
    "user_is_already_joined": True
  },
  "match_2": {
    "id": 2,
    "name": "partida2",
    "min_players": 2,
    "max_players": 2,
    "number_of_games": 113,
    "number_of_rounds": 13,
    "is_secured": False,
    "is_started": False,
    "is_finished": False,
    "creator": 5,
    'creator_name': 'juan',
    "user_id": 4,
    "user_name": "mati",
    "players": {
      "juan": {
        "robot_id": "6",
        "robot_name": "megatron"
      }
    },
    'results': {},
    "user_is_creator": False,
    "is_available_to_join": True,
    "is_available_to_leave": False,
    "is_ready_to_start": False,
    "user_is_already_joined": False
  },
    "match_3": {
    "id": 3,
    "name": "partida3",
    "min_players": 2,
    "max_players": 3,
    "number_of_games": 20,
    "number_of_rounds": 10000,
    "is_secured": False,
    "is_started": False,
    "is_finished": False,
    "creator": 1,
    'creator_name': 'angelescch',
    "user_id": 4,
    "user_name": "mati",
    "players": {
      "angelescch": {
        "robot_id": "2",
        "robot_name": "MEGATRON"
      }
    },
    'results': {},
    "user_is_creator": False,
    "is_available_to_join": True,
    "is_available_to_leave": False,
    "is_ready_to_start": False,
    "user_is_already_joined": False
  }
}

def test_get_matches_successful_case():
    response = client.get(
        "/matches",
        headers={"Authorization": token_type + " " + access_token}
    )
    assert response.status_code==status.HTTP_200_OK
    assert response.json()==matches_list

def test_get_matches_not_autheticated_user():
    response = client.get(
        "/matches",
        headers={"Authorization": token_type + " " + wrong_token}
    )
    assert response.status_code==status.HTTP_401_UNAUTHORIZED
    assert response.json()=={"detail":"Could not validate credentials"}