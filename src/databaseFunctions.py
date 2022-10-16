from pony.orm import *
from entities import *

from typing import Optional
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@db_session
def get_id_by_username(username: str):
    return User.get(username=username).id

@db_session
def get_all_usernames():
    return select(u.username for u in User)[:]

@db_session
def get_all_emails():
    return select(u.email for u in User)[:]

@db_session
def get_user_by_username(username: str):
    return User.get(username=username)

@db_session
def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user

@db_session
def upload_user(username: str, password: str,
                email: str, avatar: Optional[str]):
    if avatar is None:
        User(username=username, password=pwd_context.hash(password),
             email=email)
    else:
        User(username=username, password=pwd_context.hash(password),
             email=email, avatar=avatar)


@db_session
def user_id_is_valid(user_id: int):
    return user_id in select(u.id for u in User)[:]

@db_session
def valid_robot_for_user(user_id: int, robot_name: str):
    return not (robot_name in select(r.name for r in Robot if r.user==User[user_id])[:])


@db_session
def get_robot_by_user_and_name(user_id: int,robot_name: str):
    robot_id = select(r.id for r in Robot 
                if r.user.id==user_id and r.name==robot_name)[:1][0]
    return robot_id

# Creates a new Robot and returns it's id
# user_id_in must be a valid Id in Users.
@db_session
def upload_robot(
        user_id_in: int,
        name_in: str,
        avatar_in: Optional[str],
        behaviour_file_in:str
    ):
    
    if avatar_in!=None:
        Robot(user=User[user_id_in],
                        name=name_in,
                        avatar=avatar_in,
                        behaviour_file=behaviour_file_in)
    else:
        Robot(user=User[user_id_in],
                        name=name_in,
                        behaviour_file=behaviour_file_in)

@db_session
def get_all_matches ():
    matches = []
    matches_list = (select(m for m in Match)[:])
    for m in matches_list:
        match_dict = m.to_dict()
        users_list = []
        for us in (select(ma.users for ma in Match if ma.id == m.id)):
            users_list.append(us.to_dict())
        match_dict['users'] = users_list
        matches.append(match_dict)
    jsons = {}
    for p in matches:
        key = 'match_'+str(p['id'])
        jsons[key]=p
    return (jsons)

