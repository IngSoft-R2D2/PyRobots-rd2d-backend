from datetime import datetime, timedelta
from typing import Optional

from fastapi import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr

from databaseFunctions import *

SECRET_KEY = "afaebb3eea9e698378e76dcd26d7d46d83e45890f662d896e538edf8d5243758"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(day=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



class TokenData(BaseModel):
    username: Optional[str] = None

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

# chequear si el usuario está confirmado: dejar para caso de uso confirmar usuario (próximos sprints)
# async def get_current_confirmed_user(current_user: User = Depends(get_current_user)):
#     if not current_user.is_confirmed:
#         raise HTTPException(status_code=400, detail="The user is not confirmed")
#     return current_user


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


#listar partidas 
@app.get("/match/")
async def show_all_matches(current_user: User = Depends(get_current_user)):
	return get_all_matches()
