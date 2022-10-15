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
