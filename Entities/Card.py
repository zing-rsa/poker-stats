from Entities.Suits import Suits
from Entities.maps import valueMap

class Card():

    Id = -1
    value = -1
    suit = Suits.Undefined

    def __init__(self, _id, _value, _suit):
        self.Id = _id
        self.value = _value
        self.suit = _suit
    
    def toString(self):
        return f"{valueMap(self.value)} of {self.suit.name}"

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

