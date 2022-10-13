from fastapi import FastAPI, HTTPException, status
from databaseFunctions import *
from entities import User, Match, Robot
from pydantic import BaseModel, EmailStr

app = FastAPI()

class MatchIn(BaseModel): 
    name: str
    max_players: int
    min_players: int
    number_of_games: int
    password: str
    creator_id: int

class MatchOut(BaseModel):
	match_id: int
	operation_result: str

# TODO: implementation
@app.get("/")
async def root():
	pass

    

"""
	Registrar robot:
"""
@app.post(
	"/matches/",
	response_model=MatchOut,
	status_code=status.HTTP_201_CREATED
)
async def create_match(new_match: MatchIn) -> int:
	creator= get_user_by_id(MatchIn.creator_id)
	match_id = match_add(MatchIn.name,
                        MatchIn.max_players,
                        MatchIn.min_players,
                        MatchIn.number_of_games,
                        MatchIn.password,
                        creator)
	return MatchOut(
		new_match_id = match_id,
		operation_result = "Match succesfully created"
	)