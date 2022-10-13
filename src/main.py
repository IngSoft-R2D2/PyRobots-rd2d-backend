from datetime import datetime, timedelta
from typing import Union, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel, EmailStr

from databaseFunctions import *

SECRET_KEY = "afaebb3eea9e698378e76dcd26d7d46d83e45890f662d896e538edf8d5243758"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

app = FastAPI()

class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/login/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(day=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt










class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    avatar: Optional[str]

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
