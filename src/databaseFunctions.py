from pony.orm import *
from entities import *
from werkzeug.security import generate_password_hash, check_password_hash


@db_session
def get_all_usernames():
    select(u.username for u in User)[:]

@db_session
def get_all_emails():
    select(u.email for u in User)[:]

@db_session
def upload_user(username: str, password: str,
                email: str, avatar: Optional(str)) -> int:
    u = User(username=username, password=generate_password_hash(password),
         email=email, avatar=avatar)
    return u.id
