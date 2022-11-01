from pony.orm import *
from round import Round
from typing import (
    Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union
)

def generate_simulation(
	db: Database,
	user_id: int,
	number_of_round: int,
	robots_id: List[int]
) -> list[Round]:
	pass