# PyRobots by R2D2: Backend

## Check the API Documentation
[REST API documentation](https://grand-school-039.notion.site/REST-API-documentation-5f5dd691dd334cd188c05265d5b63c21)


## Installation

You will need a virtual environment and install the requirements
```
$ git clone https://github.com/IngSoft-R2D2/PyRobots-rd2d-backend.git
$ cd PyRobots-rd2d-backend
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Running the Server

From ```PyRobots-rd2d-backend/src``` directory, run ```uvicorn```:
```
$ uvicorn main:app --reload
```

## Testing

### Unit Test
Testing using database in RAM

From ```PyRobots-rd2d-backend/test``` directory, run ```pytest``` and ```coverage```:
```
$ coverage run -m pytest -vv && coverage report -m
```
