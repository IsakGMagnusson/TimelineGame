import random

from classes import *

games = {}


def is_card_date_in_order(cards: [Card], card_index: int) -> bool:
    left_card = cards[max(0, card_index - 1)]
    right_card = cards[min(card_index + 1, len(cards) - 1)]
    card = cards[card_index]
    return left_card["date"] <= card["date"] <= right_card["date"]


def generate_code(code_length: int):
    ascii_uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    return "".join(random.choice(ascii_uppercase + digits) for _ in range(code_length))


def sort_cards_date(cards_to_sort: []):
    return sorted(cards_to_sort, key=lambda card: card["date"])



# ----Utility----
def clamp(min_value: int, value: int, max_value: int):
    return max(min_value, min(value, max_value))


def swap(arr: [], swap1, swap2):
    arr[swap1], arr[swap2] = arr[swap2], arr[swap1]
    return arr


def next_or_cycle_index(arr: [], index: int) -> int:
    return (index + 1) if (index + 1 < len(arr)) else 0


# ----Server lookups----
def get_game(gameCode: str) -> Game:
    return games[gameCode]


def get_players(gameCode: str) -> list[Player]:
    return games[gameCode].players


def get_active_player(gameCode: str) -> Player:
    return get_players(gameCode)[get_game(gameCode).player_turn]


def get_cards(gameCode: str) -> list[Card]:
    return games[gameCode].cards


def is_player_turn(gameCode: str, player: Player) -> bool:
    return get_active_player(gameCode).name == player.name


# def get_all_cards_in_play(gamecode, player) -> []:


# ----Unused----
def swap_cards(cards: [], card_index: int, is_left: bool):
    swap_with_index = -1 if is_left else 1

    clamped_card_index = clamp(0, card_index, len(cards) - 1)
    clamped_swap_with_index = clamp(0, swap_with_index, len(cards) - 1)
    return swap(cards.copy(), clamped_card_index, clamped_swap_with_index)
