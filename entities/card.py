from util import Suits, value_map


class Card():

    counter = 0

    def __init__(self, _value, _suit):
        self.value = _value
        self.suit = _suit
        self.str = str(self.value) + self.suit.name[0]
        self.id = Card.counter
        Card.counter += 1
