from Entities.SuitsEnum import Suits
from Entities.KickerEnum import KickerEnum

class Card():

    id = -1
    value = -1
    suit = Suits.Undefined

    def __init__(self, _id, _value, _suit):
        self.id = _id
        self.value = _value
        self.suit = _suit
    
    def toString(self):
        return f"id: {self.id}, {KickerEnum(self.value).name} of {self.suit.name}"