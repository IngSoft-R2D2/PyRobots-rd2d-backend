from pony.orm import *
from typing import Optional
from passlib.context import CryptContext

"""
        Function definitions:
"""


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@db_session
def get_id_by_username(db: Database, username: str):
    return get_user_by_username(db,username).id

@db_session
def get_all_usernames(db: Database):
    return select(u.username for u in db.User)[:]

@db_session
def get_all_emails(db: Database):
    return select(u.email for u in db.User)[:]

@db_session
def get_user_by_username(db: Database, username: str):
    return db.User.get(username=username)

@db_session
def username_exists(db: Database, username: str):
    return db.User.exists(username=username)

@db_session
def authenticate_user(db: Database, username: str, password: str):
    user = get_user_by_username(db, username)
    if pwd_context.verify(password, user.password):
        return True
    return False

@db_session
def is_user_confirmed(db: Database, username: str):
    return get_user_by_username(db,username).is_confirmed

@db_session
def upload_user(db: Database, 
                username: str, password: str,
                email: str, avatar: Optional[str]):
    if avatar is None:
        db.User(username=username, password=pwd_context.hash(password),
             email=email)
    else:
        db.User(username=username, password=pwd_context.hash(password),
             email=email, avatar=avatar)

@db_session
def valid_robot_for_user(db: Database, user_id: int, robot_name: str):
    return not (robot_name in select(r.name for r in db.Robot if r.user==db.User[user_id])[:])

@db_session
def get_robot_by_user_and_name(db: Database, user_id: int,robot_name: str):
    robot_id = select(r.id for r in db.Robot
                if r.user.id==user_id and r.name==robot_name)[:1][0]
    return robot_id

@db_session
def get_match_by_creator_and_name(db: Database, creator_id: int, match_name: str):
    match_id = select(m.id for m in db.Match 
                if m.creator.id==creator_id and m.name==match_name)[:1][0]
    return match_id

# Creates a new Robot and returns it's id
# user_id_in must be a valid Id in Users.
@db_session
def upload_robot(
        db: Database,
        user_id_in: int,
        name_in: str,
        avatar_in: Optional[str],
        behaviour_file_in:str
    ):
    
    if avatar_in is None:
        db.Robot(user=db.User[user_id_in],
                    name=name_in,
                    behaviour_file=behaviour_file_in)
    else:
        db.Robot(user=db.User[user_id_in],
                name=name_in,
                avatar=avatar_in,
                behaviour_file=behaviour_file_in)


@db_session
def get_all_matches (db: Database):
    matches = []
    matches_list = (select(m for m in db.Match)[:])
    for m in matches_list:
        match_dict = m.to_dict()
        users_list = []
        for us in (select(ma.users for ma in db.Match if ma.id == m.id)):
            users_list.append(us.username)
        match_dict['users'] = users_list
        matches.append(match_dict)
    jsons = {}
    for p in matches:
        key = 'match_'+str(p['id'])
        jsons[key]=p
    return jsons

# Creates a new Match and returns it's id.
# creator_id_in must be a valid Id in Users.
@db_session
def match_add(
        db: Database,
        creator_id_in: int,
        name_in: str,
        max_players_in: int,
        min_players_in: int,
        number_of_games_in: int,
        number_of_rounds_in: int,
        password_in: Optional[str]
    ):
    if password_in is None:
        db.Match(creator=db.User[creator_id_in],
                        name=name_in,
                        max_players=max_players_in,
                        min_players=min_players_in,
                        number_of_games=number_of_games_in,
                        number_of_rounds=number_of_rounds_in,
                        users = [db.User[creator_id_in]])
    else:
        db.Match(creator=db.User[creator_id_in],
                        name=name_in,
                        max_players=max_players_in,
                        min_players=min_players_in,
                        number_of_games=number_of_games_in,
                        number_of_rounds=number_of_rounds_in,
                        password=password_in,
                        users = [db.User[creator_id_in]])

@db_session
def get_all_user_robots(db, username):
    user = get_user_by_username(db, username)
    robots_list = select(r for r in user.robots)[:]
    json = {}
    for r in robots_list:
        key = str(r.id)
        json[key]=r.name
    return json
