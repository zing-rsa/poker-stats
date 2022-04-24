from Entities.Suits import Suits
from Entities.Card import Card
from Entities.Player import Player
from Entities.HandEnum import handEnum
from Entities.Hand import Hand
import math
import pprint

class PokerStatter():
    
    def __init__(self):
        pass
    
    def evaluate(self, table):

        # getAllPossibleHands()
        # assignHandChances()
        # isolatedHandChances()
        # generateOutcomes()
        # assignPlayerChances()
        
        pass
    
    def assignPossibleHands(self,table):
        for p in table.players:
            p.possibleHands = self.getPossibleHands(p)
    
    def getPossibleHands(self, player):
        possibleHands = []

        possibleHands = possibleHands + self.possibleOnePairs(p)
        possibleHands = possibleHands + self.possibleTwoPairs(p)
        possibleHands = possibleHands + self.possibleTrips(p)
        possibleHands = possibleHands + self.possibleStrights(p)
        possibleHands = possibleHands + self.possibleFlush(p)
        possibleHands = possibleHands + self.possibleFullHouses(p)
        possibleHands = possibleHands + self.possibleQuads(p)
        possibleHands = possibleHands + self.possibleStraightFlushes(p)
        possibleHands = possibleHands + self.possibleRoyalFlushes(p)

        return possibleHands

    def assignHandChances(self, table):
        
        for p in table.players:
            for hand in p.possibleHands:
                if len(outs) > table.cardsToFlip:
                    hand.chance = 0
                    continue

                outsfound = [False] * len(hand.outs)
                for i, o in enumerate(hand.outs):
                    for c in table.deck:
                        if c.suit == o.suit and c.value == o.value:
                            outsFound[i] = True

                if False in outsFound:
                    hand.chance = 0
                    continue
                
                # figure out probs

                # remove all 0's

    def isolateHandChances(self, table):
        for p in table.players:
            for hand in p.possibleHands:
                for out in hand.outs:
                    # sum all other outs
                    # multiply out.chance by (1 - sum(all other outs.chance))
                    pass

    def generateOutcomes(self, table):
        for p in table.players:
            for hand in p.hands:
                # get all opponent hands that beat this hand

                # get chance of those hands occuring

                # create outcome obj
                # chance = hand.chance * (1 - sum(opponent outs chance))
                pass
    
    def assignPlayerChances(self, table):

        for p in table.players:
            chance = 0
            for outcome in p.outcomes:
                chance = chance + outcome.chance # TODO: create outcome object
            p.chance = chance
        
