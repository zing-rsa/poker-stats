import enum
from functools import total_ordering

class Hand():

   counter = 0

   def __init__(self, name, cards, chance, outs):
        self.name = name
        self.cards = sorted(cards,key=lambda c: c.toShortString())
        self.cardstr = ','.join([c.toShortString() for c in self.cards])
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
   default = 0
   highCard = 1
   onePair = 2
   twoPair = 3
   trips = 4
   straight = 5
   flush = 6
   fullHouse = 7
   quads = 8
   straightFlush = 9

   def __lt__(self, other):
      if self.__class__ is other.__class__:
         return self.value < other.value
      return NotImplemented