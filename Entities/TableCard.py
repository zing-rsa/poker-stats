from Entities.Suits import Suits
from Entities.Kicker import KickerEnum

class TableCard():
    id = -1
    value = -1
    suit = Suits.Undefined
    visible = True

    def __init__(self, _id, _value, _suit, _visible):
        self.id = _id
        self.value = _value
        self.suit = _suit
        self.visible = _visible
    
    def toString(self):
        return f"{str(KickerEnum(self.value).name).replace('_','')} of {self.suit.name}"

    def toShortString(self):
        return f"{str(self.value)}{str(self.suit.name)[0]}"