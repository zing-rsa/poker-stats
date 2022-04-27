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
        twopairs = []
        
        for c, card in enumerate(player.visibleCards):
            nextCard = player.visibleCards[(c+1) % len(player.visibleCards)]
            for i in range(4):
               if suitMap[i] != card.suit:
                   for j in range(4):
                       if suitMap[j] != nextCard.suit:
                           outs = [
                               Card(card.value, suitMap[i]),
                               Card(nextCard.value, suitMap[j])
                           ]

                           twopairs.append(Hand(
                               name=Hands.twoPair,
                               cards=[
                                   card,
                                   outs[0],
                                   nextCard,
                                   outs[1]
                               ],
                               chance=None,
                               outs=outs
                           ))

        return twopairs

    def possibleTrips(self, player):
        trips = []
        alreadyCalculated = []

        for card in player.visibleCards:
            tableMatches = [c for c in player.visibleCards if c.value == card.value and c.suit != card.suit]

            if len(tableMatches) == 0:
                otherSuits = [suit for suit in Suits if suit != card.suit]

                trips += [
                    Hand(
                       name=Hands.trips,
                       cards=[
                           card,
                           Card(card.value, otherSuits[0]),
                           Card(card.value, otherSuits[1])
                       ],
                       chance=None,
                       outs=[
                           Card(card.value, otherSuits[0]),
                           Card(card.value, otherSuits[1])
                       ]
                    ),
                    Hand(
                        name=Hands.trips,
                        cards=[
                            card,
                            Card(card.value, otherSuits[0]),
                            Card(card.value, otherSuits[2])
                        ],
                        chance=None,
                        outs=[
                            Card(card.value, otherSuits[0]),
                            Card(card.value, otherSuits[2])
                        ]
                    ),
                    Hand(name=Hands.trips,
                       cards=[
                           card,
                           Card(card.value, otherSuits[1]),
                           Card(card.value, otherSuits[2])
                       ],
                       chance=None,
                       outs=[
                           Card(card.value, otherSuits[1]),
                           Card(card.value, otherSuits[2])
                       ]
                    )
                ]
            elif len(tableMatches) > 0:
                if card.value not in alreadyCalculated:
                    alreadyCalculated.append(card.value)
                    otherSuits = [suit for suit in Suits if suit not in [card.suit,tableMatches[0].suit]]

                    outs = [
                        Card(card.value, otherSuits[0]),
                        Card(card.value, otherSuits[1])
                    ]
                    trips += [
                        Hand(
                            name=Hands.trips,
                            cards=[
                                card,
                                tableMatches[0],
                                outs[0]
                            ],
                            chance=None,
                            outs=[
                                outs[0]
                            ]
                        ),
                        Hand(
                            name=Hands.trips,
                            cards=[
                                card,
                                tableMatches[0],
                                outs[1]
                            ],
                            chance=None,
                            outs=[
                                outs[1]
                            ]
                        )
                    ]

        #print(':'.join(h.cardsString for h in trips))
        return trips

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
