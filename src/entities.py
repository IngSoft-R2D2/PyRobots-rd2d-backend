from pony.orm import *

db = Database()

# class definitions

class User(db.Entity):
    username = Required(str, unique=True)
    password = Required(str)
    email = Required(str, unique=True)
    is_confirmed = Required(bool, default=False, sql_default='0')
    avatar = Optional(str)
    
class Partida(db.Entity):
    id = PrimaryKey(int, auto=True)
    Nombre = Required(str)
    jugadores_max = Required(int)
    jugadores_min = Required(int)
    cant_juegos = Optional(int)
    clave = Optional(str)
    
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
