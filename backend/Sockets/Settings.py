from flask_socketio import emit
from extensions import socketio
from functions import *
from settings.cardGenerator import get_cards_from_selected_settings
from settings.settings import all_settings
from tests.testdata import *

@socketio.on("confirm_settings")
def confirm_settings(gameCode, confirmedSettings, win_score):
    cards = testcards
    # cards = get_cards_from_selected_settings(confirmedSettings)
    random.shuffle(cards)
    get_cards(gameCode).extend(cards)
    # Assign starting timeline-card to players
    for player in games[gameCode].players:
        for x in range(15):
            card = get_game(gameCode).draw_card()
            card["state"] = Card_State.LOCKED
            player.timeline.append(card)
        socketio.emit(
            "game_start", {"timeline": player.timeline}, room=player.socket_id
        )

    # Set gamedata
    games[gameCode].score_to_win = win_score
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
            "score_to_win": games[gameCode].score_to_win,
        },
        room=get_game(gameCode).socket_id,
    )