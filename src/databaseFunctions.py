from pony.orm import *
from entities import *

"""
        Function definitions:
"""

def user_in_database(user_id: str):
    return set[]!=User.select()[:]


def get_user_by_id(user_id: int):


# Creates a new Robot and returns it's id.
def robot_add(
    user_id_in: int,
    name_in: str,
    avatar_in: str,
    behaviour_file_in:str
):
    with db_session:
        owner_user = get(u for u in User if u.id==user_id)
        new_robot = Robot(user=owner_user,
        name=name_in,
        avatar=avatar_in,
        behaviour=behaviour_file_in)
    return new_robot.id

    
