from entities.suits import Suits
from entities.card import Card
from entities.player import Player
from entities.hand import Hand, Hands
from util import valueMap, suitMap


class Pokerstatter():

    def __init__(self):
        pass

    def evaluate(self, table):

        self.assignPossibleHands(table)
        # assignHandChances()
        # isolateHandChances()
        # generateOutcomes()
        # assignPlayerChances()

        pass

    def assignPossibleHands(self, table):
        for p in table.players:
            p.possibleHands = p.possibleHands + self.possibleOnePairs(p)
            p.possibleHands = p.possibleHands + self.possibleTwoPairs(p)
            p.possibleHands = p.possibleHands + self.possibleTrips(p)
            p.possibleHands = p.possibleHands + self.possibleStraights(p)
            p.possibleHands = p.possibleHands + self.possibleFlush(p)
            p.possibleHands = p.possibleHands + self.possibleFullHouses(p)
            p.possibleHands = p.possibleHands + self.possibleQuads(p)
            p.possibleHands = p.possibleHands + self.possibleStraightFlushes(p)
            p.possibleHands = p.possibleHands + self.possibleRoyalFlushes(p)

            self.removeDupes(p)

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
                chance = chance + outcome.chance  # TODO: create outcome object
            p.chance = chance

    def removeDupes(self, player):

        dupes = []

        for i, hand in enumerate(player.possibleHands):
            for j in range(i+1, len(player.possibleHands)):
                if (player.possibleHands[j].cardsString == hand.cardsString 
                        and player.possibleHands[j].name == hand.name):
                    dupes.append(hand.id)

        player.possibleHands = [h for h in player.possibleHands if h.id not in dupes]
        print('nothing')

    def possibleOnePairs(self, player):
        # do we include the table one pairs or just the one pairs for our player?

        onepairs = []

        for card in player.visibleCards:
            for i in range(4):
                if suitMap[i] != card.suit:
                    out = Card(card.value, suitMap[i])
                    onepairs.append(Hand(
                        name=Hands.onePair,
                        cards=[card, out],
                        chance=None,
                        outs=[out]
                    ))

        return onepairs

    def possibleTwoPairs(self, player):
        #twopairs = []
        #
        # for i in range(4):
        #    if suitMap[i] != player.cards[0].suit:
        #        for j in range(4):
        #            if suitMap[j] != player.cards[1].suit:
        #                outs = [
        #                    Card(player.cards[0].value, suitMap[i]),
        #                    Card(player.cards[1].value, suitMap[j])
        #                ]
        #
        #                twopairs.append(Hand(
        #                    name=Hands.twoPair,
        #                    cards=[
        #                        player.cards[0],
        #                        outs[0],
        #                        player.cards[1],
        #                        outs[1]
        #                    ],
        #                    chance=None,
        #                    outs=outs
        #                ))

        # return twopairs

        # what if we get two of the same value?

        return []

    def possibleTrips(self, player):
        return []

    def possibleStraights(self, player):
        return []

    def possibleFlush(self, player):
        return []

    def possibleFullHouses(self, player):
        return []

    def possibleQuads(self, player):
        return []

    def possibleStraightFlushes(self, player):
        return []

    def possibleRoyalFlushes(self, player):
        return []
