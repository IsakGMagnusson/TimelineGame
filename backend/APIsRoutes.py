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
    isGameCodeValid = bool(gamecode in games)
    return {"isGameCodeValid": isGameCodeValid}
