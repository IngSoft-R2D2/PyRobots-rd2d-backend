from pony.orm import *

db = Database()

# class definitions

class User(db.Entity):
    username = Required(str, unique=True)
    password = Required(str)
    email = Required(str, unique=True)
    is_confirmed = Required(bool, default=False, sql_default='0')
    avatar = Optional(str)

class Robot(db.Entity):
    id = PrimaryKey(int,auto=True) # Clave primaria, no se si hace falta, capaz q si por la relacion
    user = Required(User) 
    name = Required(str)
    avatar = Optional(str)
    behavior_file = Required(str)
    matches_played = Required (int,default=0) 
    matches_won = Required(int, default=0)
    matches_lost = Required(int, default=0)
    matches_drawed = Required(int, default=0)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)