import math
from pony.orm import *
from typing import (
    Dict, List, Optional, Tuple
)
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
    return pwd_context.verify(password, user.password)

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

# List all matches adding information relatively to the user.
@db_session
def get_all_matches(db: Database, user_id: int):
    matches_list = []
    matches = select(m for m in db.Match)[:]
    for match in matches:
        match_dict = match.to_dict()
        match_dict['user_id'] = user_id
        match_not_full =  len(match.users) < match.max_players
        user_is_creator = db.User[user_id] == match.creator
        user_in_match = db.User[user_id] in match.users
        match_players_quantity_satisfied = (len(match.users) >= match.min_players and
                                             len(match.users) < match.max_players)

        # add usernames with robot names.
        robots_in_match = {}
        for r_data in select((r.id, r.name, r.user.username) for r in match.robots)[:]:
            robot_data_dict = {}
            robot_id = str(r_data[0])
            robot_name = str(r_data[1])
            robot_user_name = str(r_data[2])
            robot_data_dict['robot_id'] = robot_id
            robot_data_dict['robot_name'] = robot_name
            robots_in_match[robot_user_name] = robot_data_dict
        match_dict['players'] = robots_in_match
        
        # add control attributes.
        match_dict['user_is_creator'] = db.User[user_id] == match.creator
        match_dict['is_available_to_join'] = (not match.is_started and not match.is_finished 
                                                and match_not_full and not user_is_creator)
        match_dict['is_available_to_leave'] = (not match.is_started and not match.is_finished
                                                and user_in_match and not user_is_creator)
        match_dict['is_ready_to_start'] = (not match.is_started and not match.is_finished
                                            and match_players_quantity_satisfied)
        match_dict['user_is_already_joined'] = user_in_match
        matches_list.append(match_dict)

    matches_to_json = {}
    for match in matches_list:
        key = 'match_'+str(match['id'])
        matches_to_json[key] = match
    return matches_to_json

# Creates a new Match.
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
    if password_in is None or password_in == "":
        db.Match(creator=db.User[creator_id_in],
            name=name_in,
            max_players=max_players_in,
            min_players=min_players_in,
            number_of_games=number_of_games_in,
            number_of_rounds=number_of_rounds_in,
            robots = [db.Robot[robot_id_in]],
            users = [db.User[creator_id_in]]
        )
    else:
        db.Match(creator=db.User[creator_id_in],
            name=name_in,
            max_players=max_players_in,
            min_players=min_players_in,
            number_of_games=number_of_games_in,
            number_of_rounds=number_of_rounds_in,
            robots=[db.Robot[robot_id_in]],
            users=[db.User[creator_id_in]],
            is_secured=True,
            password = pwd_context.hash(password_in)
        )

@db_session
def get_all_user_robots(db, username) -> Dict:
    user = get_user_by_username(db, username)
    robots_list = select(r for r in user.robots)[:]
    robots_json = {}
    for r in robots_list:
        key = str(r.id)
        robot_info = {}
        robot_info['name'] = r.name
        robot_info['avatar'] = r.avatar
        robot_info['matches_played'] = r.matches_played
        robot_info['matches_won'] = r.matches_won
        robot_info['matches_lost'] = r.matches_lost
        robot_info['matches_tied'] = r.matches_tied
        robots_json[key] = robot_info
    return robots_json

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
def is_secured_match(
        db: Database,
        match_id: int
    ):
    return db.Match[match_id].is_secured

@db_session
def is_valid_password(
        db: Database,
        match_id: int,
        password: str
    ):
    return pwd_context.verify(password, db.Match[match_id].password)

@db_session
def get_robot_name_in_match(
        db: Database,
        match_id: int,
        user_id: int
    ):
    return select(r.name for r in db.Match[match_id].robots if r.user==db.User[user_id])[:][0]

@db_session
def get_robot_name_by_id(
        db: Database,
        robot_id: int
    ):
    return db.Robot[robot_id].name

@db_session
def get_user_creator_by_robot_id(
        db: Database,
        robot_id: int
    ):
    return db.Robot[robot_id].user.username

@db_session
def user_is_creator_of_match(db, match_id, user_id):
    return db.Match[match_id].creator.id == user_id

@db_session
def start_match_db(
        db: Database,
        match_id: int
    ):
    db.Match[match_id].is_started = True

@db_session
def update_robots_statistics(
        db: Database,
        match_results: dict
    ):
    winner_exists: bool = False
    games_won_highest = -math.inf
    winners_id: List[int] = []

    # find the winners id's and the games it/they won.
    for robot_id in match_results:
        # new potential winner found.
        if match_results[robot_id]['won_games'] > games_won_highest:
            winners_id.clear()
            winners_id.append(robot_id)
            games_won_highest = match_results[robot_id]['won_games']
        # another robot has the same games won.
        elif match_results[robot_id]['won_games'] == games_won_highest:
            winners_id.append(robot_id)
    
    winner_exists = len(winners_id) == 1
    # update statistics.
    for robot_id in match_results:
        db.Robot[robot_id].matches_played += 1
        # is the winner robot.
        if winner_exists and robot_id in winners_id:
            db.Robot[robot_id].matches_won += 1
        # is a loser robot.
        elif winner_exists and not (robot_id in winners_id):
            db.Robot[robot_id].matches_lost += 1
        # not a winner nor a loser.
        elif not winner_exists and robot_id in winners_id:
            db.Robot[robot_id].matches_tied += 1
        # is a loser robot.
        elif not winner_exists and not (robot_id in winners_id):
            db.Robot[robot_id].matches_lost += 1

@db_session
def end_match_db(
        db: Database,
        match_id: int
    ):
    db.Match[match_id].is_finished = True

@db_session
def is_match_started(db, match_id):
    return db.Match[match_id].is_started

@db_session
def valid_number_of_players(db, match_id):
    users_list = select(u for u in db.Match[match_id].users)[:]
    return db.Match[match_id].min_players <= len(users_list) <= db.Match[match_id].max_players

# Returns (z,x,y) where z robots_id's, x number of games and y number of rounds.
@db_session
def get_match_parameters(
        db: Database,
        match_id: int
    ) -> Tuple[List[int], int, int]:
    robot_ids_list: List[int] = []
    robots: List[Robot] = db.Match[match_id].robots
    for r in robots:
        robot_ids_list.append(r.id)
    params: Tuple[List[int], int, int] = (
        robot_ids_list, 
        db.Match[match_id].number_of_games, 
        db.Match[match_id].number_of_rounds
    )
    return params

@db_session
def generate_robots_for_game(
        db: Database,
        robots_id: "list[int]"
    ) -> List[Robot]:
    robots: List[Robot] = []
    index = 1
    for r_id in robots_id:
        r = db.Robot[r_id]
        user_id = db.Robot[r_id].user.id
        filename_path = f"robots/user_id_{user_id}/"+r.behaviour_file
        exec(open(filename_path).read(), globals())
        without_suffix = r.behaviour_file.removesuffix('.py')
        words_list_lowercase = without_suffix.split('_')
        words_list_capitalize = [word.capitalize() for word in words_list_lowercase]
        class_name = ''.join(words_list_capitalize)
        robot_name = f"R{index}_{r.name}"
        to_execute = "bot = " + class_name + "(\"" + robot_name  + "\"" + ", " + str(r_id) + ")"
        ldict = {}
        exec(to_execute, globals(),ldict)
        bot = ldict['bot']
        robots.append(bot)
        index += 1
    return robots
