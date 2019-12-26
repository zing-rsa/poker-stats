
from Entities.Suits import Suits
from Entities.Card import Card
import math
import random

class Dealer():

    def generateDeck(self):
        outDeck = []
        for i in range(0,52):
            tempCard = Card(i, (i%13)+1, Suits(math.floor(i/13)+1))
            outDeck.append(tempCard)
        return outDeck

    def dealCards(self):
        pass

    def produceRandomCard(self, deck):
        index = random.randint(0,51)
        tempCard = deck[index]
        return tempCard



             



        