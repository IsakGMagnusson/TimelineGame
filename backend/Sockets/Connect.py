from typing import List
from flask import request
from flask_socketio import emit
from classes import Game, Player
from extensions import socketio
from functions import *
from tests.testdata import *
import time

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_send_pong")
def user_send_pong(gamecode, player_name):
    get_game(gamecode).pings_from_players.append(player_name)

@socketio.on("create_game")
def create_game():
    gamecode = generate_code(1)
    game = Game(request.sid, gamecode)
    # Add (gamecode, gamestate) to hashmap
    games.update({gamecode: game})
    socketio.emit("create_game", {"gamecode": gamecode}, room=game.socket_id)
    init_pinging(gamecode)

def init_pinging(gamecode):
    while True:
        send_pings(gamecode)
        time.sleep(3)
        handle_pongs(gamecode)
        time.sleep(3)

def send_pings(gamecode):
    for player in get_players(gamecode):
        socketio.emit(
            "server_send_ping",
            room=player.socket_id,
        )

def handle_pongs(gamecode):
    if len(get_players(gamecode)) == 0:
        return
    
    for player in get_players(gamecode):
        player.isConnected = player.name in get_game(gamecode).pings_from_players

    if(not get_game(gamecode).is_game_started):
        handle_disconnects_before_gamestart(gamecode)
    elif(get_game(gamecode).is_game_started):
        handle_disconnects_during_game(gamecode)
    
    get_game(gamecode).pings_from_players = []

def handle_disconnects_before_gamestart(gamecode):
    get_game(gamecode).players = [x for x in get_game(gamecode).players if x.isConnected]
    socketio.emit(
        "users", 
        {"joinedPlayerNames": [x.name for x in get_game(gamecode).players]}, 
        room=get_game(gamecode).socket_id
    )

def handle_disconnects_during_game(gamecode):
    disconnectedPlayerNames = [x.name for x in get_game(gamecode).players if not x.isConnected]
    
    socketio.emit(
        "inform_disconnect",
        {"disconnected_players": disconnectedPlayerNames},
        room=get_game(gamecode).socket_id,
    )

    for player in get_players(gamecode):
        socketio.emit(
            "send_disconnected_playernames",
            {"playernames": disconnectedPlayerNames},
            room=player.socket_id,
        )

@socketio.on("user_join")
def handle_user_join(gameCode, name):
    if not get_game(gameCode).is_game_started:
        player = Player(request.sid, name)
        games[gameCode].players.append(player)
        get_game(gameCode).pings_from_players.append(player.name)
    
    elif get_game(gameCode).is_game_started:
        socketio.emit(
            "reconnect",
            {"disconnectedPlayers": [x.name for x in get_game(gameCode).players if not x.isConnected]},
            room=request.sid,
        )

@socketio.on("reconnect")
def reconnect(gameCode, name):
    for player in get_players(gameCode):
        if player.name == name:
            player.socket_id = request.sid
            get_game(gameCode).pings_from_players.append(player.name)
            socketio.emit(
                "reconnect_as_player",
                {"isMyTurn": is_player_turn(gameCode, player)},
                room=player.socket_id,
            )
