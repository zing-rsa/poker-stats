from entities.suits import Suits
from util import valueMap

class Card():

    counter = 0

    def __init__(self, _value, _suit):
        self.value = _value
        self.suit = _suit
        self.id = Card.counter
        Card.counter += 1
    
    def toString(self):
        return f"{valueMap[self.value]} of {self.suit.name}"

    def toShortString(self):
        return f"{str(self.value)}{str(self.suit.name)[0]}"
    
    def getSuitShort(self):
        if self.suit == Suits.Clubs:
            return "C"
        elif self.suit == Suits.Spades:
            return "S"
        elif self.suit == Suits.Hearts:
            return "H"
        elif self.suit == Suits.Diamonds:
            return "D"
        else:
            return "default"

