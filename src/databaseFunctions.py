from pony.orm import *
from entities import *

# function definitions

# Example: 
#   def show_users():
#       with db_session:
#           User.select().show()

@db_session

def get_all_matches ():
	return (select (m for m in Match).show())