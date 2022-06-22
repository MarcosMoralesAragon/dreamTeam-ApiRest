import string

from fastapi import FastAPI, Body
from starlette.middleware.cors import CORSMiddleware
import service

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/registerUser")
def create_user(user_data: dict = Body(...)):
    return service.create_new_user(user_data)


@app.post("/get")
def get_user(email: dict = Body(...)):
    return service.get_user(email)


@app.post("/createLeague")
def create_league(data: dict = Body(...)):
    return service.create_new_league(data)


@app.post("/spectateLeague")
def spectate_league(data: dict = Body(...)):
    return service.espectate_new_league(data)


@app.post("/getLeague")
def get_league(data: dict = Body(...)):
    return service.get_league(data)


@app.post("/getLeagues")
def get_leagues(data: dict = Body(...)):
    return service.get_leagues(data)


@app.post("/createPlayer")
def create_new_player(data: dict = Body(...)):
    return service.create_new_player(data)


@app.post("/getPlayers")
def get_players(data: dict):
    return service.get_players(data)

@app.get("/getAllPlayers")
def get_all_players():
    return service.get_all_players()

@app.post("/createMatch")
def create_new_match(data: dict = Body(...)):
    return service.create_new_match(data)


@app.post("/getMatches")
def get_matches(data: dict = Body(...)):
    return service.get_matches(data)

@app.post("/endMatch")
def end_match(data: dict = Body(...)):
    return service.end_match(data)