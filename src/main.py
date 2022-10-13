from fastapi import FastAPI
from databaseFunctions import *


app = FastAPI()

# TODO: implementation
@app.get("/")
async def root():
	pass

def get_all_matches ():
	
	return
# TODO: add endpoints

#listar partidas 
@app.get("/match/")
async def show_all_matches():
	return get_all_matches()
