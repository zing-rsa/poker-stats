from Entities.SuitsEnum import Suits

class Card():

    id = -1
    value = -1
    suit = Suits.Undefined

    def __init__(self, _id, _value, _suit):
        self.id = _id
        self.value = _value
        self.suit = _suit
