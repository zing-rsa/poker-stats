from Entities.Player import Player
from Entities.Dealer import Dealer
from Entities.TableCard import TableCard

class Table():

    deck = []
    players = []
    tableCards = []
    visibleTableCards = []
    audienceVisibleCards = []
    invisibleCards = []

    def __init__(self, _playerCount):
        self.playerCount = _playerCount
        for i in range(0, self.playerCount):
            self.players.append(Player(i, []))

        self.dealer = Dealer()
        self.dealer.dealCards()

        self.tableCards = []
        self.visibleTableCards = []
        self.audienceVisibleCards = []
        self.invisibleCards = []
    
    def startNewHand(self):
        self.assignPlayerCards()
        self.assignTableCards()

    def nextBettingRound(self):
        self.tableCards = self.dealer.flipCard(self.tableCards)
        
    def assignTableCards(self):
        self.tableCards = self.dealer.produceTableCards()

    def assignPlayerCards(self):
        playerCardList = self.dealer.producePlayerCards(len(self.players))
        i = 0
        for cardSet in playerCardList:
            self.players[i].cards = cardSet
            i=i+1

    def getVisibleCards(self, pIndex):
        cardsOut = []

        for c in self.tableCards:
            if c.visible:
                cardsOut.append(c)

        for c in self.players[pIndex].cards:
            cardsOut.append(c)

        return cardsOut

    def getAudienceVisibleCards(self):
        cardsOut = []

        for c in self.tableCards:
            if c.visible:
                cardsOut.append(c)

        for c in self.players:
            for i in range(2):
                cardsOut.append(c.cards[i])

        return cardsOut

    def getAllCardsDict(self):

        cardsDict = {}

        for p in self.players:
            cardsDict[p.Id] = p.cards
        
        tableCards = []

        for c in self.tableCards:
            if c.visible:
                tableCards.append(c)
        cardsDict["TableCards"] = tableCards

        return cardsDict


    
    


        