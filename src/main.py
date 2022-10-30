import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from email_validator import validate_email
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr

from databaseFunctions import *
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from jinja2 import Environment, select_autoescape, PackageLoader

from fastapi.responses import RedirectResponse

from entities import define_database

app = FastAPI()

def get_db():
    return define_database()

SECRET_KEY = "afaebb3eea9e698378e76dcd26d7d46d83e45890f662d896e538edf8d5243758"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


origins = {
    "http://localhost",
    "http://localhost:3000",
}

app.add_middleware(
   CORSMiddleware,
    allow_origins = origins,
    allow_credentials =True,
    allow_methods = ["*"],
    allow_headers= ["*"],
)

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
    robot_id: int
    max_players: Optional[int] = None
    min_players: Optional[int] = None
    number_of_games: int
    number_of_rounds: int
    password: Optional[str] = None

class NewMatchOut(BaseModel):
    match_id: int
    operation_result: str

class JoinMatchOut(BaseModel):
    operation_result: str

class User(BaseModel):
    username: str
    email: EmailStr
    avatar: Optional[str] = None

class UserIn(User):
    password: str

class UserDb(User):
    id: int

class LeaveMatchOut(BaseModel):
    operation_result: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    id: Optional[int] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        token: str = Depends(oauth2_scheme), db: Database = Depends(get_db)
    ):
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
    user = get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


# TODO: implementation
@app.get("/")
async def root():
    pass


"""
send email
"""
load_dotenv('.env')
conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_FROM = os.getenv('MAIL_FROM'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
    MAIL_PORT = os.getenv('MAIL_PORT'),
    MAIL_SERVER = os.getenv('MAIL_SERVER'),
    MAIL_FROM_NAME = os.getenv('MAIL_FROM_NAME'),
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    TEMPLATE_FOLDER = './templates'
)

env = Environment(
    loader=PackageLoader('templates', ''),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template(f'email.html')

async def send_email_async(email_to: EmailStr, username: str, code: str):
    message = MessageSchema(
        subject = 'PyRobots: Validation Code',
        recipients = [email_to],
        body = template.render(username = username, code = code),
        subtype = 'html',
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name='email.html')


"""
    Create user.
"""
@app.post(
    "/users/",
    status_code=status.HTTP_201_CREATED
)
async def create_user(new_user: UserIn, db: Database = Depends(get_db)):
    if new_user.username in get_all_usernames(db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="A user with this username already exists"
        )
    if new_user.email in get_all_emails(db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="A user with this email already exists"
        )
    if not valid_password(new_user.password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Invalid password format"
        )
    try:
        existing_email = validate_email(new_user.email)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Email address does not exist"
        ) from None
    upload_user(db, new_user.username, new_user.password,
                new_user.email, new_user.avatar)
    id = get_id_by_username(db, new_user.username)
    code = create_access_token({'sub': new_user.username, 'id': id})
    await send_email_async(new_user.email, new_user.username, code)
    return {'operation_result':
                'Verification code successfully sent to your email'}

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
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Database = Depends(get_db)
    ):
    if not username_exists(db, form_data.username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This username does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not authenticate_user(db, form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not is_user_confirmed(db, form_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user is not confirmed"
        )
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
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
    current_user: User = Depends(get_current_user), db: Database = Depends(get_db)):
    user_id = get_id_by_username(db, current_user.username)
    if not valid_robot_for_user(db, user_id, robot_to_cr.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This user has a robot with this name already."
        )
    upload_robot(db,
        user_id,
        robot_to_cr.name,
        robot_to_cr.avatar,
        robot_to_cr.behaviour_file
    )
    new_robot_id = get_robot_by_user_and_name(db,
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
    current_user: User = Depends(get_current_user), db: Database = Depends(get_db)):
    user_id = get_id_by_username(db, current_user.username)
    valid_match_config(match_to_cr)
    match_add(db,
        user_id,
        match_to_cr.name,
        match_to_cr.robot_id,
        match_to_cr.max_players,
        match_to_cr.min_players,
        match_to_cr.number_of_games,
        match_to_cr.number_of_rounds,
        match_to_cr.password
    )
    new_match_id = get_match_by_creator_and_name(db,
        user_id,
        match_to_cr.name
    )
    return NewMatchOut(
        match_id=new_match_id,
        operation_result="Successfully created."
    )

def valid_match_config(match: NewMatchIn):
    if (match.max_players is None):
        match.max_players = 4
    if (match.min_players is None):
        match.min_players = 2
    if (match.max_players<2 or match.max_players>15):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid maximum number of players."
        )
    if (match.min_players<2):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid minimum number of players."
        )
    if (match.min_players > match.max_players):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Minimum number of players must not be greater than the maximun number of players."
        )
    if (match.number_of_games>200 or match.number_of_games<1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid number of games."
        )
    if (match.number_of_rounds>10000 or match.number_of_rounds<1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid number of rounds."
        )


"""
    List joinable matches.
"""
@app.get("/matches/join")
async def show_joinable_matches(current_user: User = Depends(get_current_user),
                                  db: Database = Depends(get_db)):
    return get_joinable_matches(db, current_user.id)

"""
    List matches to begin.
"""
@app.get("/matches/begin")
async def show_matches_to_begin(current_user: User = Depends(get_current_user),
                                  db: Database = Depends(get_db)):
    return get_matches_to_begin(db, current_user.id)


"""
    List robots.
"""
@app.get("/robots/")
async def list_user_robots(current_user: User = Depends(get_current_user), db: Database = Depends(get_db)):
    return get_all_user_robots(db, current_user.username)


"""
    Verify code
"""
@app.get("/user/", response_class=RedirectResponse,
         response_description="Account verified successfully"
        )
async def verify_user(
        validation: str,
        db: Database = Depends(get_db)
    ):
    validation_exception = HTTPException(
        status_code=status.HTTP_302_FOUND,
        detail="Could not validate account",
        headers = {"Location": "http://localhost:3000/"}
    )
    try:
        payload = jwt.decode(validation, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        id: int = payload.get('id')
        if username is None or id is None:
            raise validation_exception
        token_data = TokenData(username=username, id=id)
    except JWTError:
        raise validation_exception
    id_in_db = get_id_by_username(db, token_data.username)
    if token_data.id != id_in_db:
        raise validation_exception
    confirm_user(db, id_in_db)
    return "http://localhost:3000/home"

"""
    Join match.
"""
@app.put(
    "/matches/join/{match_id}robot{robot_id}",
    response_model = JoinMatchOut,
    status_code = status.HTTP_200_OK
)
async def join_match(
        match_id: int,
        robot_id: int,
        current_user: UserDb = Depends(get_current_user),
        db: Database = Depends(get_db)
    ):
    if not match_exists(db=db, match_id=match_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found."
        )
    if user_in_match(
            db=db,
            user_id=current_user.id,
            match_id=match_id
        ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is in match already."
        )
    add_user_with_robot_to_match(
        db=db,
        match_id=match_id,
        user_id=current_user.id,
        robot_id=robot_id
    )
    return JoinMatchOut(
            operation_result="Successfully joined."
        )


"""
    Leave match.
"""
@app.put(
    "/matches/leave/{match_id}",
    response_model = LeaveMatchOut,
    status_code = status.HTTP_200_OK
)
async def leave_match(
        match_id: int,
        current_user: UserDb = Depends(get_current_user),
        db: Database = Depends(get_db)
    ):
    if not match_exists(db=db, match_id=match_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found."
        )
    if not user_in_match(
            db=db,
            user_id=current_user.id,
            match_id=match_id
        ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in the given match."
        )
    if user_is_creator_of_the_match(
            db=db,
            user_id=current_user.id,
            match_id=match_id
        ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Creator of the match is not allowed to leave."
        )
    remove_user_with_robots_from_match(
        db,
        match_id=match_id,
        user_id=current_user.id
    )
    return LeaveMatchOut(
            operation_result="Successfully abandoned."
        )
