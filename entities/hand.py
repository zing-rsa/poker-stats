import enum
from util import handScores
from functools import total_ordering

class Hand():

    counter = 0

    def __init__(self, name, owner, cards, kickers=None):
        self.name = name
        self.owner = owner
        self.kickers = kickers
        self.cards = cards
        self.cardstr = ','.join([c.str for c in self.cards])

        self.rank = self.getHandRank()
        self.id = Hand.counter
        Hand.counter += 1

    def getHandRank(self):
        base = handScores[self.name.name]

        if self.name.name in ['highCard','onePair', 'trips','quads', 'straight', 'straightFlush']:
            return base + self.cards[0].value
        elif self.name.name in ['twoPair', 'fullHouse']:
            return base + self.cards[0].value + (self.cards[-1].value/14)
        elif self.name.name == 'flush':
            return base + self.cards[0].value
        elif self.name.name == 'royalFlush':
            return base
        else:
            pass

    def toString(self):

        outstring = self.name + ": ["
        comma = ""

        for c in self.cards:
            outstring += comma + c.str
            comma = ","
        outstring += "]"

        return outstring


@total_ordering
class Hands(enum.Enum):
    highCard = 1
    onePair = 2
    twoPair = 3
    trips = 4
    straight = 5
    flush = 6
    fullHouse = 7
    quads = 8
    straightFlush = 9
    royalFlush = 10

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
