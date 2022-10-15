from fastapi import FastAPI
from databaseFunctions import *
from fastapi.responses import JSONResponse

app = FastAPI()

# TODO: implementation
@app.get("/")
async def root():
	pass

# TODO: add endpoints

#listar partidas 
@app.get("/match/")
async def show_all_matches(): 
	return get_all_matches()
