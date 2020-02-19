from Entities.HandEnum import handEnum

class Player():

    Id = -1
    cards = []
    currentHighestHand = handEnum.default
    handChances = {}
    handsToCheck = []

    def __init__(self, _Id, _cards):
        self.Id = _Id
        self.cards = _cards

    def toString(self):
        return f"Id: {self.Id}, Cards: {self.cards[0].toString()}, {self.cards[1].toString()}"