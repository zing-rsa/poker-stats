from entities.suits import Suits
from entities.card import Card
from entities.player import Player
from entities.hand import Hand, Hands
from util import valueMap, suitMap


class Pokerstatter():

    counter = 0
    availableCards = []
    playerStore = []

    def __init__(self):
        pass

    def evaluate(self, table):
        self.availableCards = table.deck
        self.playerStore = [p for p in table.players]
        tablecards = [s.card for s in table.slots if s.visible]

        self.completeTable(tablecards, 0, 5 - len(tablecards))

    def completeTable(self, tableCards, previousIteration, cardsToFlip):
        if cardsToFlip:
            for i, card in enumerate(self.availableCards):
                if i < previousIteration:
                    continue
                
                newTableCards = [c for c in tableCards] + [card]
                self.completeTable(newTableCards, i, cardsToFlip-1)

        else:
            self.processOutcome()
        
    def processOutcome(self):
        self.counter += 1


