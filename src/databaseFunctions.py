from pony.orm import *
from entities import *

from typing import Optional


@db_session
def user_id_is_valid(user_id: str):
    return user_id in select(u.id for u in User)[:]

@db_session
def get_robot_by_user_and_name(user_id: int,robot_name: str):
    robot_id = select(r.id for r in Robot 
                if r.user.id==user_id and r.name==robot_name)[:1][0]
    return robot_id

# Creates a new Robot and returns it's id
# user_id_in must be a valid Id in Users.
@db_session
def create_robot(
        user_id_in: int,
        name_in: str,
        avatar_in: Optional[str],
        behaviour_file_in:str
    ):
    
    if avatar_in!=None:
        Robot(user=User[user_id_in],
                        name=name_in,
                        avatar=avatar_in,
                        behaviour_file=behaviour_file_in)
    else:
        Robot(user=User[user_id_in],
                        name=name_in,
                        behaviour_file=behaviour_file_in)
