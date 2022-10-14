from fastapi import *
from databaseFunctions import *
from typing import Optional
from pydantic import BaseModel, EmailStr


app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    avatar: Optional[str] = None

class UserOut(BaseModel):
    id: int
    operation_result: str


# TODO: implementation
@app.get("/")
async def root():
	pass


# create a user: registro de usuario
@app.post(
    "/users/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
async def create_user(new_user: UserIn) -> int:
    if new_user.username in get_all_usernames():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="A user with this username already exists"
        )
    if new_user.email in get_all_emails():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="A user with this email already exists"
        )
    upload_user(new_user.username, new_user.password,
                new_user.email, new_user.avatar)
    return UserOut(
        id = get_id_by_username(new_user.username),
        operation_result="Succesfully created!")
