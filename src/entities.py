from pony.orm import *

# class definitions
def define_entities(db):
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
        min_players = Required(int)
        max_players = Required(int)
        number_of_games = Required(int)
        number_of_rounds = Required(int)
        password = Optional(str)
        is_finished = Required(bool, default=False, sql_default='0')
        users = Set(User, reverse='matches')
        creator = Required(User, reverse='created_matches')

    class Robot(db.Entity):
        id = PrimaryKey(int,auto=True)
        user = Required(User)
        name = Required(str)
        avatar = Optional(str)
        behaviour_file = Required(str)
        matches_played = Required (int,default=0)
        matches_won = Required(int, default=0)
        matches_lost = Required(int, default=0)
        matches_drawed = Required(int, default=0)
        composite_key(user, name)


def define_database():
    db = Database(**db_prod)
    define_entities(db)
    db.generate_mapping(create_tables=True)
    return db

db_prod = {'provider':'sqlite', 'filename':'database.sqlite', 'create_db':True}
db_test = {'provider':'sqlite', 'filename':':sharedmemory:'}
