import unittest


class Test_is_card_position_correct(unittest.TestCase):
    mock_card2 = {'text': '2', 'date': '1500'}
    mock_card3 = {'text': '3', 'date': '2500'}

    def test_leftmost_correct(self):
        mock_active_cards =  [{'text': 'a', 'date': 1000}, {'text': 'b', 'date': 2000}, {'text': 'c', 'date': 3000}, {'text': 'd', 'date': 4000}]
        mock_selected_card = {'text': '1', 'date': 500}
        isCorrect = is_card_position_correct(mock_active_cards, mock_selected_card, 0)
        self.assertTrue(isCorrect)


def is_card_position_correct(activeCards, cardToCheck, cardPosition) -> bool:
    isCorrect = False
    activeCards.insert(cardPosition, cardToCheck)


    if(cardPosition == 0):
        if(activeCards[cardPosition]["date"] <= activeCards[cardPosition+1]["date"]):
            isCorrect = True
    elif (cardPosition == len(activeCards)-1):
            if(activeCards[cardPosition]["date"] >= activeCards[cardPosition-1]["date"]):
                isCorrect = True
    else:
        if (activeCards[cardPosition]["date"] >= activeCards[cardPosition-1]["date"] and 
            activeCards[cardPosition]["date"] <= activeCards[cardPosition+1]["date"]):
            isCorrect = True
    

    return isCorrect


if __name__ == '__main__':
    unittest.main()