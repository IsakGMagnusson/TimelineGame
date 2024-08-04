from extensions import socketio
from functions import *
from tests.testdata import *
from engineio.payload import Payload
from Sockets.Settings import *
from Sockets.Gameplay import *
from Sockets.Fetch import *
from Sockets.Connect import *

# https://github.com/zauberzeug/nicegui/issues/209
Payload.max_decode_packets = 50

@socketio.on("confirm_settings")
def socket_confirm_settings(gameCode, confirmedSettings, win_score):
    confirm_settings(gameCode, confirmedSettings, win_score)

@socketio.on("move_card")
def socket_move_card(gameCode, move_to_index):
    move_card(gameCode, move_to_index)

@socketio.on("put_card")
def socket_put_card(gameCode):
    put_card(gameCode)

@socketio.on("draw_card_or_new_turn")
def socket_draw_card_or_new_turn(gameCode):
    draw_card_or_new_turn(gameCode)

@socketio.on("draw_card")
def socket_draw_card(gameCode):
    draw_card(gameCode)

@socketio.on("go_next_turn")
def socket_go_next_turn(gameCode):
    go_next_turn(gameCode)

@socketio.on("fetch_cards")
def socket_fetch_cards(gameCode):
    fetch_cards(gameCode)

@socketio.on("fetch_all_settings")
def socket_fetch_all_settings():
    fetch_all_settings()

@socketio.on("connect")
def socket_handle_connect():
    handle_connect()

@socketio.on("user_send_pong")
def socket_user_send_pong(gamecode, player_name):
    user_send_pong(gamecode, player_name)

@socketio.on("create_game")
def socket_create_game():
    create_game()

@socketio.on("user_join")
def socket_handle_user_join(gameCode, name):
    handle_user_join(gameCode, name)

@socketio.on("reconnect")
def socket_reconnect(gameCode, name):
    reconnect(gameCode, name)

@socketio.on("scroll_cards")
def socket_scroll_cards(gameCode, scroll_percent):
    scroll_cards(gameCode, scroll_percent)
