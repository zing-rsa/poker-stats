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

            evalCards = sorted(player.cards + tableCards, key=lambda c: c.value)

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
            
            hand = self.getRoyal(suitGroups, player)
            if hand:
                playerHands += [hand]
                continue
            
            hand = self.getStraightFlush(suitGroups, player)
            if hand:
                playerHands += [hand]
                continue
            
            hand = self.getQuads(valueGroups, evalCards, player)
            if hand:
                playerHands += [hand]
                continue
            
            hand = self.getFullHouse(valueGroups, player)
            if hand:
                playerHands += [hand]
                continue

            hand = self.getFlush(suitGroups, player)
            if hand:
                playerHands += [hand]
                continue
            
            hand = self.getStraight(evalCards, player)
            if hand:
                playerHands += [hand]
                continue
            
            hand = self.getTrips(valueGroups, evalCards, player)
            if hand:
                playerHands += [hand]
                continue
            
            hand = self.getTwoPair(valueGroups, evalCards, player)
            if hand:
                playerHands += [hand]
                continue

            hand = self.getOnePair(valueGroups, evalCards, player)
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
                if p.id == winner.owner:
                    p.wins += 1
    
    def getRoyal(self, suits, player):
        straightFlush = self.getStraightFlush(suits, player)
        if straightFlush and sorted(straightFlush.cards, key=lambda c: c.value)[0].value == 10:
            return Hand(
                Hands.royalFlush,
                valueSum=sum(c.value for c in straightFlush.cards),
                owner=player.id,
                cards=straightFlush.cards
            )
        return None

    def getStraightFlush(self, suits, player):

        for key, val in suits.items():
            if len(val) >= 5:
                cards = sorted(val, key=lambda c: c.value, reverse=True)

                if cards[0].value == 14:
                    cards = cards + [Card(1, cards[0].suit)]

                seqCards = []
                for c in cards:
                    if not seqCards or seqCards[-1].value - c.value == 1:
                        seqCards.append(c)
                    elif seqCards[-1].value - c.value > 1:
                        seqCards = [c]

                    if len(seqCards) == 5:
                        if seqCards[-1].value == 1:
                            seqCards[-1] = Card(14, seqCards[-1].suit)

                        return Hand(
                            name=Hands.straight,
                            valueSum=sum(c.value for c in seqCards),
                            owner=player.id,
                            cards=seqCards
                        )
        return None

    def getQuads(self, values, cards, player):
        for key, val in values.items():
            if len(val) == 4:
                cards = val + [sorted([c for c in cards if c.value != key], key=lambda c: c.value, reverse=True)[0]]
                return Hand(
                    name=Hands.quads,
                    valueSum=sum(c.value for c in cards),
                    owner=player.id,
                    cards=cards
                )
        return None

    def getFullHouse(self, values, player):
        trips = []
        dubs = []
        for key, val in values.items():
            if len(val) == 3:
                trips = val
                break
        for key, val in values.items():
            if len(val) == 2:
                dubs = val
                #don't break incase there is a higher pair
        if trips and dubs:
            cards = trips + dubs
            return Hand(
                name=Hands.fullHouse,
                valueSum=sum(c.value for c in cards),
                owner=player.id,
                cards=cards
            )
            
        return None

    def getFlush(self, suits, player):
        hand = None
        for key, val in suits.items():
            if len(val) >= 5:
                cards=sorted(val, key=lambda c: c.value, reverse=True)[:5]
                return Hand(
                    name=Hands.flush,
                    valueSum=sum(c.value for c in cards),
                    owner=player.id,
                    cards=cards
                )

        return None

    def getStraight(self, cards, player):
        cards = sorted(cards, key=lambda c: c.value, reverse=True)

        if cards[0].value == 14:
            cards = cards + [Card(1, cards[0].suit)]

        seqCards = []
        for c in cards:
            if not seqCards or seqCards[-1].value - c.value == 1:
                seqCards.append(c)
            elif seqCards[-1].value - c.value > 1:
                seqCards = [c]
            
            if len(seqCards) == 5:
                if seqCards[-1].value == 1:
                    seqCards[-1] = Card(14, seqCards[-1].suit)

                return Hand(
                    name=Hands.straight,
                    valueSum=sum(c.value for c in seqCards),
                    owner=player.id,
                    cards=seqCards
                )
        return None

    def getTrips(self, values, cards, player):
        for key, val in values.items():
            if len(val) == 3:
                cards = val + sorted([c for c in cards if c.value != key], key=lambda c: c.value, reverse=True)[:2]
                return Hand(
                    name=Hands.trips,
                    valueSum=sum(c.value for c in cards),
                    owner=player.id,
                    cards=cards
                )
        return None

    def getTwoPair(self, values, cards, player):
        pairs = [v for k, v in values.items() if len(v) == 2]
        if len(pairs) > 1:
            highPairs = sorted(pairs, key=lambda p: p[0].value, reverse=True)[:2]
            cards = highPairs[0] + highPairs[1] + [max([c for c in cards if c.value not in [highPairs[0][0].value, highPairs[1][0].value]], key=lambda c: c.value)]
            return Hand(
                name=Hands.twoPair,
                valueSum=sum(c.value for c in cards),
                owner=player.id,
                cards=cards
            )
        return None

    def getOnePair(self, values, cards, player):
        for key, val in values.items():
            if len(val) == 2:
                cards = val + sorted([c for c in cards if c.value != key], key=lambda c: c.value, reverse=True)[:3]
                return Hand(
                    name=Hands.onePair,
                    valueSum=sum(c.value for c in cards),
                    owner=player.id,
                    cards=cards
                )
        return None

    def getHighCard(self, cards, player):
        cards = cards[-5:]
        return Hand(
            name=Hands.highCard,
            valueSum=sum(c.value for c in cards),
            owner=player.id,
            cards=cards
        )

