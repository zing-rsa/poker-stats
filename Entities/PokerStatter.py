from entities.suits import Suits
from entities.card import Card
from entities.player import Player
from entities.hand import Hand, Hands
from util import valueMap, suitMap


class Pokerstatter():

    outcomes = []
    counter = 0

    def __init__(self):
        pass

    def evaluate(self, table):
        for player in table.players:
            player.wins = 0
            player.ties = 0
        
        self.table = table
        tablecards = [s.card for s in self.table.slots if s.visible]

        self.completeTable(tablecards, 0, 5 - len(tablecards))

    def completeTable(self, tableCards, previousIteration, cardsToFlip):
        if cardsToFlip:
            for i, card in enumerate(self.table.deck):
                if i < previousIteration:
                    continue
                
                if [c for c in tableCards if c.str == card.str]:
                    continue

                newTableCards = [c for c in tableCards] + [card]
                self.completeTable(newTableCards, i, cardsToFlip-1)
        else:
            self.processOutcomes(tableCards)
        
    def processOutcomes(self, tableCards):
        playerHands = []

        for i, player in enumerate(self.table.players):

            evalCards = player.cards + tableCards

            valueGroups = {}
            suitGroups = {}
            for card in evalCards:
                if card.suit in suitGroups:
                    suitGroups[card.suit] += [card]
                else:
                    suitGroups[card.suit] = [card]
                if card.value in valueGroups:
                    valueGroups[card.value] += [card]
                else:
                    valueGroups[card.value] = [card]
            

            hand = self.getFlush(suitGroups, player)
            if hand:
                playerHands += [hand]
                continue
                
            hand = self.getHighCard(evalCards, player)
            playerHands += [hand]

        winner = max(playerHands, key=lambda h: h.rank)

        if len([h.rank for h in playerHands if h.rank == winner.rank]) > 1:
            tie=True
            for hand in playerHands:
                if hand.rank == winner.rank:
                    for p in self.table.players:
                        if p.id == hand.owner:
                            p.ties += 1
        else:
            for p in self.table.players:
                if p.id == hand.owner:
                    p.wins += 1
    
    def isStraightFlush(self,cards):
        pass

    def isQuads(self,cards):
        pass       

    def isFullHouse(self,cards):
        pass    

    def getFlush(self, suits, player):
        hand = None
        for key, val in suits.items():
            if len(val) >= 5:
                cards=sorted(val, key=lambda c: c.value, reverse=True)[0:4]
                return Hand(
                    name=Hands.flush,
                    valueSum=sum(c.value for c in cards),
                    owner=player.id,
                    cards=cards
                )

        return None


    def isStraight(self,cards):
        pass    

    def isTrips(self,cards):
        pass    

    def isTwoPair(self,cards):
        pass    

    def isOnePair(self,cards):
        pass    

    def getHighCard(self, _cards, player):
        cards = sorted(_cards, key=lambda c: c.value, reverse=True)[0:4]
        return Hand(
            name=Hands.highCard,
            valueSum=sum(c.value for c in cards),
            owner=player.id,
            cards=cards
        )

