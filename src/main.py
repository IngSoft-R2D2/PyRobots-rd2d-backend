from fastapi import *
from databaseFunctions import *
from entities import *
from pydantic import BaseModel, EmailStr

app = FastAPI()

class RobotIn(BaseModel):
    user_id: int
    name: str
    avatar: str
    behaviour_file: str

class RobotOut(BaseModel):
	robot_id: int
	operation_result: str

# TODO: implementation
@app.get("/")
async def root():
	pass


user = Required(User) 
    name = Required(str)
    avatar = Optional(str)
    behaviour_file = Required(str)
    

"""
	Registrar robot:
"""
@app.post(
	"/robots/",
	response_model=RobotOut,
	status_code=status.HTTP_201_CREATED
)
async def register_robot(new_robot: RobotIn) -> int:
	owner_user = get_user_by_id(RobotIn.user_id)
	robot_id = add_robot(
					owner_user,
					RobotIn.name,
					RobotIn.avatar,
					RobotIn.behaviour_file
	)
	return RobotOut(
		robot_id=robot_id,
		operation_result="Robot succesfully created."
	)