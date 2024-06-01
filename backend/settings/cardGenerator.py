from itertools import compress
import json
import pip._vendor.requests
from datetime import datetime
from .settings import *
from classes import Card


def get_cards_from_selected_settings(selected_settings) -> list:
    cards = []
    for setting in list(compress(all_settings, selected_settings)):
        cards.extend(get_cards_from_one_setting(setting))
    return cards


def get_cards_from_one_setting(setting: Setting):
    cards = []
    for wiki_return_value in wiki_lookup(setting.get_query()):
        card = Card(
            get_question_from_setting_type(wiki_return_value, setting.get_type()),
            datetime.strptime(
                wiki_return_value["date"]["value"], "%Y-%m-%dT%H:%M:%S%z"
            ).year,
        )
        cards.append(card.toJson())
    return cards


def wiki_lookup(query) -> list:
    url = "https://query.wikidata.org/sparql"
    return pip._vendor.requests.get(
        url, params={"format": "json", "query": query}
    ).json()["results"]["bindings"]
