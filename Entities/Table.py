from Entities.Player import Player
from Entities.Dealer import Dealer
from Entities.TableSlot import TableSlot

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

        self.tableCards = []

        tableCards = self.dealer.produceTableCards()

        for i in range(0,5):
            self.tableCards.append(TableSlot(i, False, tableCards[i]))


    def assignPlayerCards(self):
        playerCardList = self.dealer.producePlayerCards(len(self.players))
        i = 0
        for cardSet in playerCardList:
            self.players[i].cards = cardSet
            i=i+1

    def getLeftOverCards(self):
        return self.dealer.produceLeftOverCards()

    def getVisibleCards(self, pIndex):
        cardsOut = []

        for s in self.tableCards:
            if s.visible:
                cardsOut.append(s.card)

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
        tableCards = []
        cardsDict["leftOverCards"] = []
        cardsDict["TableCards"] = []

        for p in self.players:
            cardsDict[p.Id] = p.cards
        
        for s in self.tableCards:
            if s.visible:
                cardsDict["TableCards"].append(s.card)
            else:
                cardsDict["leftOverCards"].append(s.card)

        cardsDict["leftOverCards"] += self.getLeftOverCards()

        return cardsDict

    def seed(self, playerCards = None, tableCards = None):
        # expects playercards = [[cardId,cardId],[cardId,cardId],[cardId,cardId]]
        # expects tablecards = [cardId,cardId,cardId,..]

        self.players = []
        self.tableCards = []

        self.dealer = Dealer()

        playerCount = 0
        usedCards = []

        for cardIdList in playerCards:
            self.players.append(Player(playerCount, [self.dealer.getCard(cardIdList[0]), self.dealer.getCard(cardIdList[1])]))
            usedCards += [cardIdList[0],cardIdList[1]] 
            playerCount = playerCount + 1
        
        for i in range(0,5):
            if tableCards[i] is not None:
                self.tableCards.append(TableSlot(i, False, self.dealer.getCard(tableCards[i])))
                usedCards.append(tableCards[i])
            else:
                self.tableCards.append(TableSlot(i, False, self.dealer.produceRandomCard()))
        
        self.dealer.usedCards += usedCards

        
        
            






    
    


        