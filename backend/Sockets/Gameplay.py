from flask_socketio import emit
from extensions import socketio
from functions import *
from tests.testdata import *
import math
from Sockets.Settings import *

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
    for player in get_players(gameCode):
        if is_player_turn(gameCode, player):
            player.controller_state = Controller_State.AWAITING_RESPONSE
        else: 
            player.controller_state = Controller_State.INACTIVE
        socketio.emit(
            "set_controller_state",
            {"controller_state": player.controller_state},
            room=player.socket_id,
        )

    sorted_cards = sort_cards_date(
        get_active_player(gameCode).get_all_non_removed_cards()
    )
    sorted_cards.insert(get_game(gameCode).card_index, get_game(gameCode).active_card)

    # If answer correct
    if is_card_date_in_order(sorted_cards, get_game(gameCode).card_index):
        get_active_player(gameCode).place_card(get_game(gameCode).active_card)

        # If won
        if len(get_active_player(gameCode).get_all_non_removed_cards()) >= get_game(gameCode).score_to_win:
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

    get_game(gameCode).active_card = Card("", 0)
    
    
@socketio.on("draw_card_or_new_turn")
def draw_card_or_new_turn(gameCode):
    for player in get_players(gameCode):
        if is_player_turn(gameCode, player):
            player.controller_state = Controller_State.TURN_DECISION
        else: 
            player.controller_state = Controller_State.INACTIVE
        socketio.emit(
            "set_controller_state",
            {"controller_state": player.controller_state},
            room=player.socket_id,
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

    for player in get_players(gameCode):
        if is_player_turn(gameCode, player):
            player.controller_state = Controller_State.ACTIVE
        else: 
            player.controller_state = Controller_State.INACTIVE
        socketio.emit(
            "set_controller_state",
            {"controller_state": player.controller_state},
            room=player.socket_id,
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
        if is_player_turn(gameCode, player):
            player.controller_state = Controller_State.ACTIVE
        else: 
            player.controller_state = Controller_State.INACTIVE
        socketio.emit(
            "set_controller_state",
            {"controller_state": player.controller_state},
            room=player.socket_id,
        )

@socketio.on("scroll_cards")
def scroll_cards(gameCode, scroll_percent):
    emit(
        "scroll_cards",
        {"scroll_percent": scroll_percent},
        room=get_game(gameCode).socket_id,
    )