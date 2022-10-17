from datetime import datetime, timedelta
from typing import Optional

from fastapi import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr

from databaseFunctions import *


app = FastAPI()

SECRET_KEY = "afaebb3eea9e698378e76dcd26d7d46d83e45890f662d896e538edf8d5243758"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()



class UserOut(BaseModel):
    id: int
    operation_result: str


class RobotRegIn(BaseModel):
    name: str
    avatar: Optional[str] = None
    behaviour_file: str

class RobotRegOut(BaseModel):
    id: int
    operation_result: str

class NewMatchIn(BaseModel):
    name: str
    max_players: int
    min_players: int
    number_of_games: int
    number_of_rounds: int
    password: str

class NewMatchOut(BaseModel):
    match_id: int
    operation_result: str

class User(BaseModel):
    username: str
    email: EmailStr
    avatar: Optional[str] = None
    # is_confirmed: Optional[bool] = None         # dejar para caso de uso: confirmar usuario

class UserIn(User):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(day=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user

# TODO: implementation
@app.get("/")
async def root():
    pass

# chequear si el usuario está confirmado: dejar para caso de uso confirmar usuario (próximos sprints)
# async def get_current_confirmed_user(current_user: User = Depends(get_current_user)):
#     if not current_user.is_confirmed:
#         raise HTTPException(status_code=400, detail="The user is not confirmed")
#     return current_user
"""
    Create user.
"""
@app.post(
    "/users/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
async def create_user(new_user: UserIn):
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
    if not valid_password(new_user.password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Invalid password format"
        )
    upload_user(new_user.username, new_user.password,
                new_user.email, new_user.avatar)
    return UserOut(
        id = get_id_by_username(new_user.username),
        operation_result="Succesfully created!")

def valid_password(password: str) -> bool:
    l, u, d = 0, 0, 0
    validation = False
    if (len(password) >= 8):
        for i in password:
            if (i.islower()):
                l+=1
            if (i.isupper()):
                u+=1
            if (i.isdigit()):
                d+=1
    if (l>=1 and u>=1 and d>=1 and l+u+d==len(password)):
        validation = True
    return validation


"""
    Login.
"""
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


"""
    Register robot.
"""
@app.post(
    "/robots/",
    response_model=RobotRegOut,
    status_code=status.HTTP_201_CREATED
)
async def register_robot(
    robot_to_cr: RobotRegIn,
    current_user: User = Depends(get_current_user)):
    user_id = get_id_by_username(current_user.username)
    if not valid_robot_for_user(user_id, robot_to_cr.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This user has a robot with this name already."
        )
    upload_robot(
        user_id,
        robot_to_cr.name,
        robot_to_cr.avatar,
        robot_to_cr.behaviour_file
    )
    new_robot_id = get_robot_by_user_and_name(
        user_id,
        robot_to_cr.name
    )
    return RobotRegOut(
        id=new_robot_id,
        operation_result="Successfully created." 
    )


"""
    Create Match.
"""
@app.post(
    "/matches/",
    response_model=NewMatchOut,
    status_code=status.HTTP_201_CREATED
)
async def create_match(
    match_to_cr: NewMatchIn,
    current_user: User = Depends(get_current_user)):
    user_id = get_id_by_username(current_user.username)
    match_add(
        user_id,
        match_to_cr.name,
        match_to_cr.max_players,
        match_to_cr.min_players,
        match_to_cr.number_of_games,
        match_to_cr.number_of_rounds,
        match_to_cr.password
    )
    new_match_id = get_match_by_creator_and_name(
        user_id,
        match_to_cr.name
    )
    return NewMatchOut(
        id=new_match_id,
        operation_result="Successfully created." 
    )


"""
    List matches. 
"""
@app.get("/match/")
async def show_all_matches(current_user: User = Depends(get_current_user)):
    return get_all_matches()


# ejemplo de uso: funcionalidad que requiere estar logeado
# @app.get("/path/")
# async def function_name(current_user: User = Depends(get_current_user)):
#     """  code  """
#     return 'something'

# ejemplo de uso: funcionalidad que requiere estar logeado y confirmado (próximos sprints)
# @app.get("/path/")
# async def function_name(current_user: User = Depends(get_current_confirmed_user)):
#     """  code  """
#     return 'something'
