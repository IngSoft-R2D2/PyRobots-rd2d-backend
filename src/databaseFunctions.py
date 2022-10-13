from pony.orm import *
from entities import *
from pydantic import BaseModel
#from functions import * (eliminar)
# function definitions

# Example: 
#   def show_users():
#       with db_session:
#           User.select().show()

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
		matches = Match.select()
		result = [MatchInDB.from_orm(m) for m in matches]
	return (result)