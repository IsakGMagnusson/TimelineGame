import random
from flask import request
from flask import Blueprint
from functions import *
from classes import *

lobby = Blueprint("lobby", __name__)


#@lobby.route("/CreateGame", methods=["POST"])
#def create_game():


@lobby.route("/JoinGame", methods=["POST"])
def join_game():
    gamecode = request.json["gamecode"]    
    name = request.json["name"]    
    return {"joinError": getError(gamecode, name)}

def getError(gamecode, name):
    if not bool(gamecode in games): 
        return "Invalid code"
    if get_game(gamecode).is_game_started and len(get_game(gamecode).disconnected_players) == 0:
        return "Game has started and all players are connected"
    if len(name.strip()) == 0:
        return "Name not set"
    for player in get_game(gamecode).players:
        if player.name == name:
            return "Name is taken"

    return ""



