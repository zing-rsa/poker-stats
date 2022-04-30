from entities.hand import Hands, Hand

class Player():

    def __init__(self, _Id):
        self.Id = _Id
        self.cards = [None] * 2
        self.chance = 0
        self.visibleCards = []

    def toString(self):
        return f"Id: {self.Id}, Chance: {str(self.chance)}, Cards: {self.cards[0].toShortString()}, {self.cards[1].toShortString()}"