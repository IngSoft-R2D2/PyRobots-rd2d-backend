from pony.orm import *
from entities import *
from pydantic import BaseModel
from functions import * 
#from functions import * (eliminar)
# function definitions

# Example: 
#   def show_users():
#       with db_session:
#           User.select().show()

class UserInDB(BaseModel):
    username: str 
    password: str
    email: str 
    is_confirmed: str 

class MatchInDB(BaseModel):
    id: int
    name: str
    max_players: int
    min_players: int
    number_of_games: int 
    is_finished: bool
    class Config:
        orm_mode = True

@db_session

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