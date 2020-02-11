
from Entities.Suits import Suits
from Entities.Card import Card
from Entities.TableCard import TableCard 
import math
import random

class Dealer():
    deck = []
    usedCards = []

    def __init__(self):
        self.deck = self.generateDeck()

    def generateDeck(self):
        outDeck = []
        for i in range(0,52):
            tempCard = Card(i, (i%13)+1, Suits(math.floor(i/13)+1))
            outDeck.append(tempCard)
        return outDeck

    def dealCards(self):
        pass

    def produceRandomCard(self):
        index = random.randint(0,51)
        # prevent duplication 
        while index in self.usedCards:
            index = random.randint(0,51)
        self.usedCards.append(index)
        tempCard = self.deck[index]
        return tempCard

    def producePlayerCards(self, playerCount):
        cardsOut = []

        for p in range(playerCount):
            cardsOut.append([])

        for i in range(2):
            for p in range(playerCount):
                tempCard = self.produceRandomCard()
                cardsOut[p].append(tempCard)

        return cardsOut

    def produceTableCards(self):
        cardsOut = []

        for i in range(5):
            tempCard = self.produceRandomCard()
            tempTableCard = TableCard(tempCard.Id, tempCard.value, tempCard.suit, False)
            cardsOut.append(tempTableCard)

        return cardsOut

    def produceLeftOverCards(self):
        leftoverCards = []

        for card in self.deck:
            if card.Id not in self.usedCards:
                leftoverCards.append(card)

        return leftoverCards


    def flipCard(self, tableCards):

        if not tableCards[2].visible:
            for i in range(3):
                tableCards[i].visible = True
        elif not tableCards[3].visible:
            tableCards[3].visible = True
        else: 
            tableCards[4].visible = True

        return tableCards

    def getCard(self, id):
        for card in self.deck:
            if card.Id == id:
                return card











             



        