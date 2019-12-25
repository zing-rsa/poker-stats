from Entities.GameState import GameState
from Entities.SuitsEnum import Suits
from Entities.Card import Card
import math

class Dealer():

    currentGameState = GameState([[],[],[],[],[],[]])

    def __init__(self, _suppliedGameState):
        self.currentGameState = _suppliedGameState

    def generateDeck(self):
        for i in range(1,52):
            tempCard = Card(i, (i%13)+1, Suits(math.floor(i/13)+1))
            self.currentGameState.deck.append(tempCard)
            
    def printDeck(self):
        for card in self.currentGameState.deck:
            print(card.toString()) 
        