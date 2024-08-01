from flask import request
from flask_socketio import emit
from classes import Game, Player
from extensions import socketio
from functions import *
from settings.cardGenerator import get_cards_from_selected_settings
from settings.settings import all_settings
from tests.testdata import *
import math
from threading import Timer
from engineio.payload import Payload
import time

# https://github.com/zauberzeug/nicegui/issues/209
Payload.max_decode_packets = 50

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("fetch_all_settings")
def fetch_all_settings():
    settings_descriptions = [item.get_description_json() for item in all_settings]
    emit("receive_settings", {"allSettings": settings_descriptions}, broadcast=True)

def fetch_joined_names(gameCode):
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
                if player.name not in get_game(gamecode).disconnected_players:
                    get_game(gamecode).disconnected_players.append(player.name)

    if not get_game(gamecode).is_game_started:
        for player in get_players(gamecode):
            if player.name not in get_game(gamecode).pings_from_players:
                get_game(gamecode).players = [x for x in get_game(gamecode).players if x.name != player.name]
        fetch_joined_names(gamecode)

    #if len(get_game(gamecode).disconnected_players) > 0:
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
    ping_clients(gamecode)

@socketio.on("confirm_settings")
def confirm_settings(gameCode, confirmedSettings):
    cards = testcards
    # cards = get_cards_from_selected_settings(confirmedSettings)
    random.shuffle(cards)
    get_cards(gameCode).extend(cards)
    # Assign starting timeline-card to players
    for player in games[gameCode].players:
        card = get_game(gameCode).draw_card()
        card["state"] = Card_State.LOCKED
        player.timeline.append(card)
        socketio.emit(
            "game_start", {"timeline": player.timeline}, room=player.socket_id
        )

    # Set gamedata
    games[gameCode].active_card = get_game(gameCode).draw_card()
    games[gameCode].active_card["state"] = Card_State.ACTIVE
    games[gameCode].is_game_started = True

    # set player turn
    for player in get_players(gameCode):
        socketio.emit(
            "new_turn",
            {"isMyTurn": is_player_turn(gameCode, player)},
            room=player.socket_id,
        )
    # start game
    emit(
        "game_start_host",
        {
            "is_game_started": get_game(gameCode).is_game_started,
            "active_player_name": get_active_player(gameCode).name,
        },
        room=get_game(gameCode).socket_id,
    )

@socketio.on("fetch_cards")
def fetch_cards(gameCode):
    all_cards = get_active_player(gameCode).timeline.copy()
    all_cards.insert(get_game(gameCode).card_index, get_game(gameCode).active_card)
    emit(
        "fetch_cards",
        {"all_cards": all_cards},
        room=get_game(gameCode).socket_id,
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
            {"disconnectedPlayers": get_game(gameCode).disconnected_players},
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


@socketio.on("move_card")
def move_card(gameCode, move_to_index):
    old_index = get_game(gameCode).card_index
    get_game(gameCode).card_index = clamp(
        0,
        get_game(gameCode).card_index + move_to_index,
        len(get_active_player(gameCode).get_all_non_removed_cards()),
    )
    emit(
        "move_card",
        {"new_index": get_game(gameCode).card_index, "old_index": old_index},
        room=get_game(gameCode).socket_id,
    )

@socketio.on("put_card")
def put_card(gameCode):
    sorted_cards = sort_cards_date(
        get_active_player(gameCode).get_all_non_removed_cards()
    )
    sorted_cards.insert(get_game(gameCode).card_index, get_game(gameCode).active_card)

    # If answer correct
    if is_date_in_order(sorted_cards, get_game(gameCode).card_index):
        get_active_player(gameCode).place_card(get_game(gameCode).active_card)

        # If won
        if len(get_active_player(gameCode).get_all_non_removed_cards()) == 10:
            emit(
                "player_won",
                {
                    "winner_name": get_active_player(gameCode).name,
                },
                room=get_game(gameCode).socket_id,
            )

        # If not won
        else:
            emit(
                "put_card_correct",
                {
                    "active_card": games[gameCode].active_card,
                    "all_cards": sorted_cards,
                },
                room=get_game(gameCode).socket_id,
            )

    # If answer wrong
    else:
        get_game(gameCode).active_card["state"] = Card_State.ANIMATE
        get_active_player(gameCode).change_cards_state(
            Card_State.PLACED, Card_State.ANIMATE
        )

        emit(
            "put_card_incorrect",
            {
                "sorted_cards": sorted_cards,
                "active_card": get_game(gameCode).active_card,
            },
            room=get_game(gameCode).socket_id,
        )

        get_game(gameCode).active_card["state"] = Card_State.REMOVED
        get_active_player(gameCode).change_cards_state(
            Card_State.ANIMATE, Card_State.REMOVED
        )

@socketio.on("draw_card_or_new_turn")
def draw_card_or_new_turn(gameCode):
    emit(
        "put_card_correct",
        room=get_active_player(gameCode).socket_id,
    )

@socketio.on("draw_card")
def draw_card(gameCode):
    games[gameCode].active_card = get_game(gameCode).draw_card()
    sorted_cards = sort_cards_date(
        get_active_player(gameCode).get_all_non_removed_cards()
    )
    get_game(gameCode).card_index = math.floor(len(sorted_cards) / 2)
    sorted_cards.insert(get_game(gameCode).card_index, get_game(gameCode).active_card)
    get_game(gameCode).active_card["state"] = Card_State.ACTIVE
    emit(
        "draw_card",
        {
            "all_cards": sorted_cards,
        },
        room=get_game(gameCode).socket_id,
    )

@socketio.on("go_next_turn")
def go_next_turn(gameCode):
    get_active_player(gameCode).lock_placed_cards()

    get_game(gameCode).player_turn = next_or_cycle_index(
        get_players(gameCode), get_game(gameCode).player_turn
    )

    # if get_active_player(gameCode) in get_game(gameCode).winners:
    #    go_next_turn(gameCode)

    games[gameCode].active_card = get_game(gameCode).draw_card()
    games[gameCode].active_card["state"] = Card_State.ACTIVE
    sorted_cards = sort_cards_date(
        get_active_player(gameCode).get_all_non_removed_cards()
    )
    get_game(gameCode).card_index = math.floor(len(sorted_cards) / 2)
    sorted_cards.insert(get_game(gameCode).card_index, get_game(gameCode).active_card)
    emit(
        "new_turn",
        {
            "active_card": get_game(gameCode).active_card,
            "all_cards": sorted_cards,
            "active_player_name": get_active_player(gameCode).name,
        },
        room=get_game(gameCode).socket_id,
    )

    for player in get_players(gameCode):
        socketio.emit(
            "new_turn",
            {"isMyTurn": is_player_turn(gameCode, player)},
            room=player.socket_id,
        )
