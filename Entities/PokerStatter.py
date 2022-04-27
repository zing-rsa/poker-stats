from entities.suits import Suits
from entities.card import Card
from entities.player import Player
from entities.hand import Hand, Hands

class Pokerstatter():
    
    def __init__(self):
        pass
    
    def evaluate(self, table):

        # assignPossibleHands()
        # assignHandChances()
        # isolateHandChances()
        # generateOutcomes()
        # assignPlayerChances()
        
        pass

    def assignPossibleHands(self,table):
        for p in table.players:
            p.possibleHands = p.possibleHands + self.possibleOnePairs(p)
            p.possibleHands = p.possibleHands + self.possibleTwoPairs(p)
            p.possibleHands = p.possibleHands + self.possibleTrips(p)
            p.possibleHands = p.possibleHands + self.possibleStrights(p)
            p.possibleHands = p.possibleHands + self.possibleFlush(p)
            p.possibleHands = p.possibleHands + self.possibleFullHouses(p)
            p.possibleHands = p.possibleHands + self.possibleQuads(p)
            p.possibleHands = p.possibleHands + self.possibleStraightFlushes(p)
            p.possibleHands = p.possibleHands + self.possibleRoyalFlushes(p)

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
    

    def possibleOnePairs(player):
        pass
         