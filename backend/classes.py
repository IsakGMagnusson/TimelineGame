class Game:
    def __init__(self, socket_id, gamecode):
        self.socket_id = socket_id
        self.score_to_win = 10
        self.gamecode = gamecode
        self.is_game_started = False
        self.cards = []
        self.players = []
        self.player_turn = 0
        self.active_card = Card
        self.card_index = 0
        self.winners = []
        self.pings_from_players = []


    def draw_card(self):
        card = self.cards.pop()
        return card

class Card:
    def __init__(self, question, date):
        self.question = question
        self.date = date
        self.state = Card_State.IN_PILE

    def get_date(self):
        return self.date

    def toJson(self):
        return {"question": self.question, "date": self.date, "state": self.state}

class Card_State:
    IN_PILE = 0
    LOCKED = 1
    ACTIVE = 2
    PLACED = 3
    REMOVED = 4
    ANIMATE = 5

class Player:
    def __init__(self, socket_id, name):
        self.socket_id = socket_id
        self.name = name
        self.timeline = []
        self.isConnected = True
        self.controller_state = Controller_State.ACTIVE

    def get_all_non_removed_cards(self):
        return [card for card in self.timeline if card["state"] != Card_State.REMOVED]

    def place_card(self, card: Card):
        card["state"] = Card_State.PLACED
        self.timeline.append(card)

    def lock_placed_cards(self):
        card: Card
        for card in self.timeline:
            if card["state"] == Card_State.PLACED:
                card["state"] = Card_State.LOCKED

    def change_cards_state(self, from_state: Card_State, to_state: Card_State):
        for card in self.timeline:
            if card["state"] == from_state:
                card["state"] = to_state

class Controller_State:
    ACTIVE = 0
    TURN_DECISION = 1
    AWAITING_RESPONSE = 2
    INACTIVE = 3


class Setting:
    def __init__(self, description, query, type):
        self.description = description
        self.query = query
        self.type = type

    def get_description_json(self):
        return {"description": self.description}

    def get_query(self):
        return self.query

    def get_type(self):
        return self.type
