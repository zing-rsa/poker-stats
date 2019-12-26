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
        self.dealer.dealCards()

        self.tableCards = []
        self.visibleTableCards = []
        self.audienceVisibleCards = []
        self.invisibleCards = []
    
    def startNewHand(self):
        self.deck = self.dealer.generateDeck()
        # each time you choose a card create a new list of cards 
        # and check that the same card isn't used twice

        for i in range(2):
            for p in self.players:
                tempCard = self.dealer.produceRandomCard(self.deck)
                p.cards.append(tempCard)


    def printPlayers(self):
        for c in range(2):
            for p in range(len(self.players)):
                print(f"Player: {p}, card({c}): {self.players[p].cards[c].toString()}")

    def printDeck(self):
        for card in self.deck:
            print(card.toString())

    


        