from pony.orm import *
from entities import User, Match, Robot, db

"""
        Function definitions:
"""






# Creates a new Match and returns it's id.
def match_add(
        name_in: str,
        max_players_in: int,
        min_players_in: int,
        number_of_games_in: int,
        password_in: str,
        creator_id_in: int
    ):
    with db_session:
        #TODO En la siguiente línea solía decir user_id en lugar de user_id_in
        creator_user = get(u for u in User if u.id==creator_id_in)
        new_match = Match(name=name_in,
                        max_players=max_players_in,
                        min_players=min_players_in,
                        number_of_games=number_of_games_in,
                        password=password_in,
                        creator=creator_id_in)
        return new_match.id