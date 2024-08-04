from flask import request
from flask_socketio import emit
from classes import Game, Player
from extensions import socketio
from functions import *
from tests.testdata import *
import time

def handle_connect():
    print("Client connected!")

def user_send_pong(gamecode, player_name):
    get_game(gamecode).pings_from_players.append(player_name)

def create_game():
    gamecode = generate_code(1)
    game = Game(request.sid, gamecode)
    # Add (gamecode, gamestate) to hashmap
    games.update({gamecode: game})
    socketio.emit("create_game", {"gamecode": gamecode}, room=game.socket_id)
    init_pinging(gamecode)

def init_pinging(gamecode):
    while True:
        ping_clients(gamecode)
        time.sleep(3)
        handle_pings(gamecode)
        time.sleep(3)

def ping_clients(gamecode):
    if len(get_players(gamecode)) == 0:
        return
    
    for player in get_players(gamecode):
        socketio.emit(
            "server_send_ping",
            room=player.socket_id,
        )

def handle_pings(gamecode):
    for player in get_players(gamecode):
        player.isConnected = True
        if player.name not in get_game(gamecode).pings_from_players:
            player.isConnected = False

    if not get_game(gamecode).is_game_started:
        get_game(gamecode).players = [x for x in get_game(gamecode).players if x.isConnected]
        socketio.emit(
            "users", 
            {"joinedPlayerNames": [x.name for x in get_game(gamecode).players if x.isConnected]}, 
            room=get_game(gamecode).socket_id
        )

    socketio.emit(
        "inform_disconnect",
        {"disconnected_players": [x.name for x in get_game(gamecode).players if not x.isConnected]},
        room=get_game(gamecode).socket_id,
    )
    for player in get_players(gamecode):
        socketio.emit(
            "send_disconnected_playernames",
            {"playernames": [x.name for x in get_game(gamecode).players if not x.isConnected]},
            room=player.socket_id,
        )

    get_game(gamecode).pings_from_players = []

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
