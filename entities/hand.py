import enum
from util import handScores
from functools import total_ordering

class Hand():

   counter = 0

   def __init__(self, name, valueSum, owner=None, cards=None):
        self.name = name
        self.cards = sorted(cards,key=lambda c: c.toShortString())
        self.cardstr = ','.join([c.toShortString() for c in self.cards])
        self.owner = owner
        self.valueSum = valueSum
        self.rank = valueSum + handScores[self.name.name]
        self.id = Hand.counter
        Hand.counter += 1

   def toString(self):

      outstring = self.name + ": [" 
      comma = ""

      for c in self.cards:
         outstring += comma + c.toShortString()
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