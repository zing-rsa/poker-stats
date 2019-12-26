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

    def printTableCardsExposed(self):
        for c in self.tableCards:
            print(c.toString())

    def printTableCards(self):
        for c in self.tableCards:
            if c.visible:
                print(c.toString())
            else:
                print("...")

    def printPlayers(self):
        for p in range(len(self.players)):
            for c in range(2):
                print(f"Player: {p+1}, card({c+1}): {self.players[p].cards[c].toString()}")

    def printDeck(self):
        for card in self.deck:
            print(card.toString())

    


        