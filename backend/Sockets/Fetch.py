from flask_socketio import emit
from extensions import socketio
from functions import *
from settings.settings import all_settings
from tests.testdata import *
from Sockets.Settings import *
from Sockets.Gameplay import *

@socketio.on("fetch_cards")
def fetch_cards(gameCode):
    all_cards = get_active_player(gameCode).timeline.copy()
    all_cards.insert(get_game(gameCode).card_index, get_game(gameCode).active_card)
    emit(
        "fetch_cards",
        {"all_cards": all_cards},
        room=get_game(gameCode).socket_id,
    )

@socketio.on("fetch_all_settings")
def fetch_all_settings():
    settings_descriptions = [item.get_description_json() for item in all_settings]
    emit("receive_settings", {"allSettings": settings_descriptions}, broadcast=True)