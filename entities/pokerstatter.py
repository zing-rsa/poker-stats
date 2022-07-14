from entities.card import Card
from entities.player import Player
from entities.hand import Hand
from util import Hands, value_map


class Pokerstatter():

    def __init__(self):
        self.counter = 0

    def evaluate(self, table):
        for player in table.players:
            player.wins = 0
            player.ties = 0

        self.table = table
        table_cards = [s.card for s in self.table.slots if s.visible]

        self.complete_table(table_cards, 0, 5 - len(table_cards))

        for p in self.table.players:

            for key, val in p.hands.items():
                p.hands[key] = round(val/self.counter*100, 3)

            p.wins = round(p.wins/self.counter * 100, 3)
            p.ties = round(p.ties/self.counter * 100, 3)

    def complete_table(self, table_cards, p_i, cards_to_flip):
        if cards_to_flip:
            for i, card in enumerate(self.table.deck):
                if i < p_i:
                    continue

                if [c for c in table_cards if c.str == card.str]:
                    continue

                newtable_cards = [c for c in table_cards] + [card]
                self.complete_table(newtable_cards, i, cards_to_flip-1)
        else:
            self.counter += 1
            self.process_outcomes(table_cards)

    def process_outcomes(self, table_cards):
        player_hands = []

        for i, player in enumerate(self.table.players):

            eval_cards = sorted(player.cards + table_cards,
                                key=lambda c: c.value, reverse=True)

            value_grps = {}
            suit_grps = {}
            for card in eval_cards:
                if card.suit in suit_grps:
                    suit_grps[card.suit] += [card]
                else:
                    suit_grps[card.suit] = [card]
                if card.value in value_grps:
                    value_grps[card.value] += [card]
                else:
                    value_grps[card.value] = [card]

            # region hands
            hand = self.get_royal(suit_grps, player)
            if hand:
                player_hands += [hand]
                continue

            hand = self.get_straight_flush(suit_grps, player, 'outer')
            if hand:
                player_hands += [hand]
                continue

            hand = self.get_quads(value_grps, eval_cards, player)
            if hand:
                player_hands += [hand]
                continue

            hand = self.get_full_house(value_grps, player)
            if hand:
                player_hands += [hand]
                continue

            hand = self.get_flush(suit_grps, player)
            if hand:
                player_hands += [hand]
                continue

            hand = self.get_straight(eval_cards, player)
            if hand:
                player_hands += [hand]
                continue

            hand = self.get_trips(value_grps, eval_cards, player)
            if hand:
                player_hands += [hand]
                continue

            hand = self.get_two_pair(value_grps, eval_cards, player)
            if hand:
                player_hands += [hand]
                continue

            hand = self.get_one_pair(value_grps, eval_cards, player)
            if hand:
                player_hands += [hand]
                continue

            hand = self.get_high_card(eval_cards, player)
            player_hands += [hand]
            # endregion

        wins = self.compare_kickers(self.get_max_hands(player_hands), 0)

        if len(wins) == 1:
            wins[0].owner.wins += 1
        else:
            for h in wins:
                h.owner.ties += 1

    def get_royal(self, suits, player):
        straight_flush = self.get_straight_flush(suits, player, 'inner')
        if straight_flush and sorted(straight_flush.cards, key=lambda c: c.value)[0].value == 10:
            player.hands[Hands.royal_flush] += 1
            return Hand(
                Hands.royal_flush,
                owner=player,
                cards=straight_flush.cards
            )
        return None

    def get_straight_flush(self, suits, player, caller):
        for key, val in suits.items():
            if len(val) >= 5:
                cards = val[:]

                if cards[0].value == 14:
                    cards = cards + [Card(1, cards[0].suit)]

                seq_cards = []
                for c in cards:
                    if not seq_cards or seq_cards[-1].value - c.value == 1:
                        seq_cards.append(c)
                    elif seq_cards[-1].value - c.value > 1:
                        seq_cards = [c]

                    if len(seq_cards) == 5:
                        if seq_cards[-1].value == 1:
                            seq_cards[-1] = Card(14, seqCards[-1].suit)
                        if caller == 'outer':
                            player.hands[Hands.straight_flush] += 1
                        return Hand(
                            name=Hands.straight_flush,
                            owner=player,
                            cards=seq_cards
                        )
        return None

    def get_quads(self, values, cards, player):
        for key, val in values.items():
            if len(val) == 4:
                player.hands[Hands.quads] += 1
                return Hand(
                    name=Hands.quads,
                    owner=player,
                    cards=val,
                    kickers=[[c for c in cards if c.value != key][0]]
                )
        return None

    def get_full_house(self, values, player):
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
            player.hands[Hands.full_house] += 1
            return Hand(
                name=Hands.full_house,
                owner=player,
                cards=trips+dubs
            )
        return None

    def get_flush(self, suits, player):
        for key, val in suits.items():
            if len(val) >= 5:
                player.hands[Hands.flush] += 1
                return Hand(
                    name=Hands.flush,
                    owner=player,
                    cards=val[:5],
                    kickers=val[1:5]
                )

        return None

    def get_straight(self, cards, player):

        if cards[0].value == 14:
            cards = cards + [Card(1, cards[0].suit)]

        seq_cards = []
        for c in cards:
            if not seq_cards or seq_cards[-1].value - c.value == 1:
                seq_cards.append(c)
            elif seq_cards[-1].value - c.value > 1:
                seq_cards = [c]

            if len(seq_cards) == 5:
                if seq_cards[-1].value == 1:
                    seq_cards[-1] = Card(14, seq_cards[-1].suit)
                player.hands[Hands.straight] += 1
                return Hand(
                    name=Hands.straight,
                    owner=player,
                    cards=seq_cards
                )
        return None

    def get_trips(self, values, cards, player):
        for key, val in values.items():
            if len(val) == 3:
                player.hands[Hands.trips] += 1
                return Hand(
                    name=Hands.trips,
                    owner=player,
                    cards=val,
                    kickers=[c for c in cards if c.value != key][0:2]
                )
        return None

    def get_two_pair(self, values, cards, player):
        pairs = [v for k, v in values.items() if len(v) == 2]
        if len(pairs) > 1:
            player.hands[Hands.two_pair] += 1
            return Hand(
                name=Hands.two_pair,
                owner=player,
                cards=pairs[0] + pairs[1],
                kickers=[[c for c in cards if c.value != pairs[0]
                         [0].value and c.value != pairs[1][0].value][0]]
            )
        return None

    def get_one_pair(self, values, cards, player):
        for key, val in values.items():
            if len(val) == 2:
                player.hands[Hands.one_pair] += 1
                return Hand(
                    name=Hands.one_pair,
                    owner=player,
                    cards=val,
                    kickers=[c for c in cards if c.value != key][:3]
                )
        return None

    def get_high_card(self, cards, player):
        player.hands[Hands.high_card] += 1
        return Hand(
            name=Hands.high_card,
            owner=player,
            cards=[cards[0]],
            kickers=cards[1:]
        )

    def get_max_hands(self, hands):
        all_ = [hands[0]]
        max_ = hands[0].rank
        for i in range(1, len(hands)):
            if hands[i].rank > max_:
                all_ = [hands[i]]
                max_ = hands[i].rank
            elif hands[i].rank == max_:
                all_.append(hands[i])
        return all_

    def compare_kickers(self, hands, i):
        if len(hands) == 1:
            return hands
        if hands[0].kickers is None:
            return hands
        if i == len(hands[0].kickers):
            return hands

        for h in hands:
            h.rank += h.kickers[i].value

        return self.compare_kickers(self.get_max_hands(hands), i+1)
