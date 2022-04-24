from Entities.HandEnum import handEnum
from Entities.Hand import Hand

class Player():

    def __init__(self, _Id):
        self.Id = _Id
        self.cards = [None] * 2
        self.possibleHans = []

    def toString(self):
        return f"Id: {self.Id}, Cards: {self.cards[0].toShortString()}, {self.cards[1].toShortString()}"