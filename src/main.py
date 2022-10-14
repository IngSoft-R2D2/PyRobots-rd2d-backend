from fastapi import *
from databaseFunctions import *
from entities import *
from typing import Optional
from pydantic import BaseModel, EmailStr

app = FastAPI()

class RobotRegIn(BaseModel):
    user_id: int
    name: str
    avatar: Optional[str] = None
    behavior_file: str

class RobotRegOut(BaseModel):
	id: int
	operation_result: str

# TODO: implementation
@app.get("/")
async def root():
	pass

"""
	Registrar robot.
"""
@app.post(
		"/robots/",
		response_model=RobotRegOut,
		status_code=status.HTTP_201_CREATED
	)
async def register_robot(robot_to_cr: RobotRegIn) -> int:
	if not user_id_is_valid(robot_to_cr.user_id):
		raise HTTPException(status_code=404, detail="Not valid user Id")
	create_robot(
			robot_to_cr.user_id,
			robot_to_cr.name,
			robot_to_cr.avatar,
			robot_to_cr.behavior_file
		)
	new_robot_id = get_robot_by_user_and_name(
						robot_to_cr.user_id,
						robot_to_cr.name
					)
	return RobotRegOut(
				id=new_robot_id,
				operation_result="Successfully created." 
			)