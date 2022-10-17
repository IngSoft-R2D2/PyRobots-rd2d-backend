from pony.orm import *

db = Database()

# class definitions

class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)
    password = Required(str)
    email = Required(str, unique=True)
    is_confirmed = Required(bool, default=False, sql_default='0')
    avatar = Optional(str)
    robots = Set('Robot') 
    matches = Set('Match', reverse='users')
    created_matches = Set('Match', reverse='creator')

class Match(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    max_players = Required(int)
    min_players = Required(int)
    number_of_games = Required(int)
    number_of_rounds = Required(int)
    password = Optional(str)
    is_finished = Required(bool, default=False, sql_default='0')
    users = Set(User, reverse='matches')
    creator = Required(User, reverse='created_matches')
    

class Robot(db.Entity):
    id = PrimaryKey(int,auto=True) # Clave primaria, no se si hace falta, capaz q si por la relacion
    user = Optional(User)
    name = Required(str)
    avatar = Optional(str)
    behaviour_file = Required(str)
    matches_played = Required (int,default=0)
    matches_won = Required(int, default=0)
    matches_lost = Required(int, default=0)
    matches_drawed = Required(int, default=0)
    composite_key(user, name)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
