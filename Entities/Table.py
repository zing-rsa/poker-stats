from Entities.Player import Player
from Entities.Dealer import Dealer

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
        self.deck = self.dealer.generateDeck()
        self.dealer.dealCards()
        
        self.tableCards = []
        self.visibleTableCards = []
        self.audienceVisibleCards = []
        self.invisibleCards = []
    
    def printDeck(self):
        for card in self.deck:
            print(card.toString())

    


        