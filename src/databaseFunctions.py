from pony.orm import *
from entities import *
from pydantic import BaseModel 
#from functions import * (eliminar)
# function definitions

# Example: 
#   def show_users():
#       with db_session:
#           User.select().show()

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

def get_all_matches ():
    with db_session:
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
