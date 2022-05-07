from entities.suits import Suits
from entities.card import Card
from entities.player import Player
from entities.hand import Hand, Hands
from util import valueMap, suitMap


class Pokerstatter():

    def __init__(self):
        self.counter = 0

    def evaluate(self, table):
        for player in table.players:
            player.wins = 0
            player.ties = 0

        self.table = table
        tablecards = [s.card for s in self.table.slots if s.visible]

        self.completeTable(tablecards, 0, 5 - len(tablecards))

        for p in self.table.players:
            p.wins = round(p.wins/self.counter * 100, 3)
            p.ties = round(p.ties/self.counter * 100, 3)
            for key, val in p.hands.items():
                p.hands[key] = round(val/self.counter*100, 3)

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
            self.counter += 1
            self.processOutcomes(tableCards)

    def processOutcomes(self, tableCards):
        playerHands = []

        for i, player in enumerate(self.table.players):

            evalCards = sorted(player.cards + tableCards,
                               key=lambda c: c.value, reverse=True)

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

            # region hands
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
            # endregion

        wins = self.getWinnerOrTie(self.getHighHands(playerHands), 0)

        if len(wins) == 1:
            for p in self.table.players:
                if p.id == wins[0].owner:
                    p.wins += 1
                    if hand.name in p.hands:
                        p.hands[hand.name] += 1
                    else:
                        p.hands[hand.name] = 1
        else:
            for h in wins:
                for p in self.table.players:
                    if p.id == h.owner:
                        p.ties += 1
                        if hand.name in p.hands:
                            p.hands[hand.name] += 1
                        else:
                            p.hands[hand.name] = 1
                        break



        #for h in self.getHighHands(playerHands):


        #add highest rank to a list
        # if len(list) >1
        # for h in list
        #  for i in h.kickers
        #    add kicker[i] to rank
        #    check how many hands == rank
        #      if one:
        #        tie = false
        #        h.owner.wins++
        #        break
        #  if tie:
        #    for h in hand 
        #      h.owner.ties++

        # if len([h.rank for h in playerHands if h.rank == winner.rank]) > 1:
        #     for hand in playerHands:
        #         if hand.rank == winner.rank:
        #             for p in self.table.players:
        #                 if p.id == hand.owner:
        #                     p.ties += 1

        #                     if hand.name in p.hands:
        #                         p.hands[hand.name] += 1
        #                     else:
        #                         p.hands[hand.name] = 1
        # else:
        #     for p in self.table.players:
        #         if p.id == winner.owner:
        #             p.wins += 1

        #             if hand.name in p.hands:
        #                 p.hands[hand.name] += 1
        #             else:
        #                 p.hands[hand.name] = 1

    def getRoyal(self, suits, player):
        straightFlush = self.getStraightFlush(suits, player)
        if straightFlush and sorted(straightFlush.cards, key=lambda c: c.value)[0].value == 10:
            return Hand(
                Hands.royalFlush,
                owner=player.id,
                cards=straightFlush.cards
            )
        return None

    def getStraightFlush(self, suits, player):
        for key, val in suits.items():
            if len(val) >= 5:
                cards = val[:]

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
                            owner=player.id,
                            cards=seqCards
                        )
        return None

    def getQuads(self, values, cards, player):
        for key, val in values.items():
            if len(val) == 4:
                return Hand(
                    name=Hands.quads,
                    owner=player.id,
                    cards=val,
                    kickers=[[c for c in cards if c.value != key][0]]
                )
        return None

    def getFullHouse(self, values, player):
        trips = []
        dubs = []
        for key, val in values.items():
            if len(val) == 3:
                trips = val
                for key, val in values.items():
                    if len(val) == 2:
                        dubs = val
                        break
                break
        if trips and dubs:
            return Hand(
                name=Hands.fullHouse,
                owner=player.id,
                cards=trips+dubs
                # this might need work, lookup trips rules
            )

        return None

    def getFlush(self, suits, player):
        for key, val in suits.items():
            if len(val) >= 5:
                return Hand(
                    name=Hands.flush,
                    owner=player.id,
                    cards=val[:5],
                    kickers=val[1:5]
                )

        return None

    def getStraight(self, cards, player):

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
                    owner=player.id,
                    cards=seqCards
                )
        return None

    def getTrips(self, values, cards, player):
        for key, val in values.items():
            if len(val) == 3:
                return Hand(
                    name=Hands.trips,
                    owner=player.id,
                    cards=val,
                    kickers=[c for c in cards if c.value != key][0:2]
                )
        return None

    def getTwoPair(self, values, cards, player):
        pairs = [v for k, v in values.items() if len(v) == 2]
        if len(pairs) > 1:
            return Hand(
                name=Hands.twoPair,
                owner=player.id,
                cards=pairs[0] + pairs[1],
                kickers=[[c for c in cards if c.value != pairs[0]
                         [0].value and c.value != pairs[1][0].value][0]]
            )
        return None

    def getOnePair(self, values, cards, player):
        for key, val in values.items():
            if len(val) == 2:
                return Hand(
                    name=Hands.onePair,
                    owner=player.id,
                    cards=val,
                    kickers=[c for c in cards if c.value != key][:3]
                )
        return None

    def getHighCard(self, cards, player):
        return Hand(
            name=Hands.highCard,
            owner=player.id,
            cards=[cards[0]],
            kickers=cards[1:]
        )

    def getHighHands(self, hands):
        all_ = [hands[0]]
        max_ = hands[0].rank
        for i in range(1, len(hands)):
            if hands[i].rank > max_:
                all_ = [hands[i]]
                max_ = hands[i].rank
            elif hands[i].rank == max_:
                all_.append(hands[i])
        return all_
    
    def getWinnerOrTie(self, hands, i):
        if len(hands) == 1:
            return hands
        if hands[0].kickers is None:
            return hands
        if i == len(hands[0].kickers):
            return hands
        
        for h in hands:
            h.rank += h.kickers[i].value

        return self.getWinnerOrTie(self.getHighHands(hands), i+1)
        
