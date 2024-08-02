from flask import request
from flask_socketio import emit
from classes import Game, Player
from extensions import socketio
from functions import *
from tests.testdata import *
from threading import Timer
import time

def handle_connect():
    print("Client connected!")
    
def send_joined_names(gameCode):
    player_names = []
    for player in games[gameCode].players:
        player_names.append(player.name)
    socketio.emit(
        "users", {"joinedPlayerNames": player_names}, room=get_game(gameCode).socket_id
    )

def ping_clients(gamecode):
    Timer(6, ping_clients, gamecode).start()
    if len(get_players(gamecode)) == 0:
        return
    
    for player in get_players(gamecode):
        socketio.emit(
            "server_send_ping",
            room=player.socket_id,
        )

    time.sleep(3)
    if get_game(gamecode).is_game_started:
        get_game(gamecode).disconnected_players = []
        for player in get_players(gamecode):
            if player.name not in get_game(gamecode).pings_from_players:
                get_game(gamecode).disconnected_players.append(player.name)

    if not get_game(gamecode).is_game_started:
        for player in get_players(gamecode):
            if player.name not in get_game(gamecode).pings_from_players:
                get_game(gamecode).players = [x for x in get_game(gamecode).players if x.name != player.name]
        send_joined_names(gamecode)

    socketio.emit(
        "inform_disconnect",
        {"disconnected_players": get_game(gamecode).disconnected_players},
        room=get_game(gamecode).socket_id,
    )
    for player in get_players(gamecode):
        socketio.emit(
            "send_disconnected_playernames",
            {"playernames": get_game(gamecode).disconnected_players},
            room=player.socket_id,
        )

    get_game(gamecode).pings_from_players = []

def user_send_pong(gamecode, player_name):
    get_game(gamecode).pings_from_players.append(player_name)

def create_game():
    gamecode = generate_code(1)
    game = Game(request.sid, gamecode)
    # Add (gamecode, gamestate) to hashmap
    games.update({gamecode: game})
    socketio.emit("create_game", {"gamecode": gamecode}, room=game.socket_id)
    ping_clients(gamecode)

def handle_user_join(gameCode, name):
    if not get_game(gameCode).is_game_started:
        player = Player(request.sid, name)
        games[gameCode].players.append(player)
        get_game(gameCode).pings_from_players.append(player.name)
    
    elif get_game(gameCode).is_game_started:
        socketio.emit(
            "reconnect",
            {"disconnectedPlayers": get_game(gameCode).disconnected_players},
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

