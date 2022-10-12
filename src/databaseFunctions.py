from pony.orm import *
from entities import *
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash


@db_session
def get_id_by_username(username: str):
    return User.get(username=username).id

@db_session
def get_all_usernames():
    print(select(u.username for u in User)[:])
    return select(u.username for u in User)[:]

@db_session
def get_all_emails():
    print(select(u.email for u in User)[:])
    return select(u.email for u in User)[:]

@db_session
def upload_user(username: str, password: str,
                email: str, avatar: Optional[str]):
    User(username=username, password=generate_password_hash(password),
         email=email, avatar=avatar)

# @db_session
# def get_all_competitives_games():
#     select(cg for cg in CompetitivesGame)[:]
