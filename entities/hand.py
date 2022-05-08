import enum
from util import hand_scores

class Hand():

    counter = 0

    def __init__(self, name, owner, cards, kickers=None):
        self.name = name
        self.owner = owner
        self.kickers = kickers
        self.cards = cards
        self.cardstr = ','.join([c.str for c in self.cards])

        self.rank = self.get_hand_rank()
        self.id = Hand.counter
        Hand.counter += 1

    def get_hand_rank(self):
        base = hand_scores[self.name.name]

        if self.name.name in ['high_card','one_pair', 'trips','quads', 'straight', 'straight_flush']:
            return base + self.cards[0].value
        elif self.name.name in ['two_pair', 'full_house']:
            return base + self.cards[0].value + (self.cards[-1].value/14)
        elif self.name.name == 'flush':
            return base + self.cards[0].value
        elif self.name.name == 'royal_flush':
            return base
        else:
            pass

class Hands(enum.Enum):
    high_card = 1
    one_pair = 2
    two_pair = 3
    trips = 4
    straight = 5
    flush = 6
    full_house = 7
    quads = 8
    straight_flush = 9
    royal_flush = 10
