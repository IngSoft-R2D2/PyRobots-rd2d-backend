from fastapi import FastAPI, HTTPException, status
from databaseFunctions import robot_add
from entities import User, Match, Robot
from pydantic import BaseModel, EmailStr

app = FastAPI()

class RobotIn(BaseModel):
    user_id: int
    name: str
    avatar: str
    behavior_file: str

class RobotOut(BaseModel):
	id: int
	name: str
	operation_result: str

# TODO: implementation
@app.get("/")
async def root():
	pass

"""
	Registrar robot:
"""
@app.post(
	"/robots/",
	response_model=RobotOut,
	status_code=status.HTTP_201_CREATED
)
async def register_robot(new_robot: RobotIn) -> int:
	robot_id = robot_add(new_robot.user_id,
						new_robot.name,
						new_robot.avatar,
						new_robot.behavior_file)
	return RobotOut(
		new_robot_id = robot_id,
		new_robot_name = ,
		operation_result = 
	)