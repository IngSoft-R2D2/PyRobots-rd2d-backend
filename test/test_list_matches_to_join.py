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

matches_to_join = {
        'match_10': {'creator': 2,
                    'id': 10,
                    'is_finished': False,
                    'max_players': 10,
                    'min_players': 8,
                    'name': 'fake_match_for_join_2',
                    'number_of_games': 125,
                    'number_of_rounds': 1010,
                    'password': '',
                    'users_robots': {'keyword': 'MEGATRON'}},
        'match_11': {'creator': 2,
                    'id': 11,
                    'is_finished': False,
                    'max_players': 10,
                    'min_players': 8,
                    'name': 'fake_match_for_join_3',
                    'number_of_games': 125,
                    'number_of_rounds': 1010,
                    'password': '',
                    'users_robots': {'keyword': 'MEGATRON'}},
        'match_2': {'creator': 2,
                    'id': 2,
                    'is_finished': False,
                    'max_players': 10,
                    'min_players': 8,
                    'name': 'pool',
                    'number_of_games': 125,
                    'number_of_rounds': 1010,
                    'password': '',
                    'users_robots': {'keyword': 'MEGATRON'}},
        'match_3': {'creator': 2,
                    'id': 3,
                    'is_finished': False,
                    'max_players': 5,
                    'min_players': 3,
                    'name': 'NGBI',
                    'number_of_games': 5,
                    'number_of_rounds': 10,
                    'password': 'AGSV87NG4',
                    'users_robots': {'keyword': 'MEGATRON'}},
        'match_6': {'creator': 2,
                    'id': 6,
                    'is_finished': False,
                    'max_players': 10,
                    'min_players': 8,
                    'name': 'pool3',
                    'number_of_games': 125,
                    'number_of_rounds': 1010,
                    'password': '',
                    'users_robots': {'keyword': 'MEGATRON'}}
}


def test_get_matches_to_join():
    response = client.get(
        "/matches/join",
        headers={"Authorization": token_type+" "+access_token}
        )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == matches_to_join
