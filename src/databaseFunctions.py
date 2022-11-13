from pony.orm import *
from typing import Optional
from passlib.context import CryptContext
from robot import Robot


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
        behaviour_file_path: str
    ):
    
    if avatar_in is None:
        db.Robot(user=db.User[user_id_in],
                    name=name_in,
                    behaviour_file=behaviour_file_path)
    else:
        db.Robot(user=db.User[user_id_in],
                name=name_in,
                avatar=avatar_in,
                behaviour_file=behaviour_file_path)

# Lists unfinished matches not created by the current user 
# that aren't full, where the user isn't already joined.
@db_session
def get_matches_to_join (db: Database, current_user_id: int):
    matches = []
    matches_list = (select(m for m in db.Match if m.is_finished == False and 
                           (m.creator).id != current_user_id and
                            count(m.users)<m.max_players and
                            current_user_id not in m.users.id)[:])
    for m in matches_list:
        match_dict = m.to_dict()
        users_robots_json = {}
        for ur in select((r.user.username, r.name) for r in m.robots)[:]:
            users_robots_json[str(ur[0])] = str(ur[1])
        match_dict['users_robots'] = users_robots_json
        matches.append(match_dict)
    jsons = {}
    for p in matches:
        key = 'match_'+str(p['id'])
        jsons[key]=p
    return jsons

# Lists unfinished matches created by the current user 
# that have at least the minimum ammmount of players
@db_session
def get_matches_to_start(db: Database, current_user_id: int):
    matches = []
    matches_list = (select(m for m in db.Match if m.is_finished == False and 
                           (m.creator).id == current_user_id and
                            count(m.users)>=m.min_players)[:])
    for m in matches_list:
        match_dict = m.to_dict()
        users_robots_json = {}
        for ur in select((r.user.username, r.name) for r in m.robots)[:]:
            users_robots_json[str(ur[0])] = str(ur[1])
        match_dict['users_robots'] = users_robots_json
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
        robot_id_in: int,
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
                        robots = [db.Robot[robot_id_in]],
                        users = [db.User[creator_id_in]])
    else:
        db.Match(creator=db.User[creator_id_in],
                        name=name_in,
                        max_players=max_players_in,
                        min_players=min_players_in,
                        number_of_games=number_of_games_in,
                        number_of_rounds=number_of_rounds_in,
                        password=password_in,
                        robots = [db.Robot[robot_id_in]],
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

@db_session
def confirm_user(db: Database, id: int):
    db.User[id].is_confirmed = True

@db_session
def match_exists(db:Database, match_id: int):
    return db.Match.exists(id=match_id)

@db_session
def user_in_match(
        db:Database,
        user_id:int,
        match_id: int
    ):
    return db.User[user_id] in db.Match[match_id].users

@db_session
def is_valid_robot_id(
        db: Database,
        robot_id: int
    ):
    return db.Robot.exists(id=robot_id)

@db_session
def is_robot_user(
        db: Database,
        user_id: int,
        robot_id: int
    ):
    return db.Robot[robot_id] in db.User[user_id].robots

@db_session
def room_is_full(
        db: Database,
        match_id: int
    ):
    match = db.Match[match_id]
    max_players = match.max_players
    users_number = len(select(u for u in db.Match[match_id].users)[:])
    return max_players==users_number

@db_session
def add_user_with_robot_to_match(
        db:Database,
        match_id: int,
        user_id:int,
        robot_id:int
    ):
    db.Match[match_id].users.add(db.User[user_id])
    db.Match[match_id].robots.add(db.Robot[robot_id])

@db_session
def user_is_creator_of_the_match(
        db:Database,
        user_id:int,
        match_id: int
    ):
    return db.User[user_id]==db.Match[match_id].creator

@db_session
def remove_user_with_robots_from_match(
        db: Database,
        match_id: int,
        user_id: int
    ):
    for robot in select(r for r in db.Robot if r.user==db.User[user_id]):
        db.Match[match_id].robots.remove(robot)
    db.Match[match_id].users.remove(db.User[user_id])

@db_session
def get_robot_name_in_match(
        db: Database,
        match_id: int,
        user_id: int
    ):
    return select(r.name for r in db.Match[match_id].robots if r.user==db.User[user_id])[:][1]

@db_session
def get_robot_name_by_id(
        db: Database,
        robot_id: int
    ):
    return db.Robot[robot_id].name

@db_session
def generate_robots_for_game(
        db: Database,
        user_id: int,
        robots_id: "list[int]"
    ) -> "list[Robot]":
    robots: list[Robot] = []
    index = 1
    for r_id in robots_id:
        r = db.Robot[r_id]
        filename_path = f"robots/user_id_{user_id}/"+r.behaviour_file
        exec(open(filename_path).read(), globals())
        without_suffix = r.behaviour_file.removesuffix('.py')
        words_list_lowercase = without_suffix.split('_')
        words_list_capitalize = [word.capitalize() for word in words_list_lowercase]
        class_name = ''.join(words_list_capitalize)
        robot_name = f"R{index}_{r.name}"
        to_execute = "bot = " + class_name + "(\"" + robot_name + "\")"
        ldict = {}
        exec(to_execute, globals(),ldict)
        bot = ldict['bot']
        robots.append(bot)
        index += 1
    return robots