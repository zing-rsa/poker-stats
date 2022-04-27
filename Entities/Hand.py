import enum

class Hand():

   def __init__(self, name, cards, chance, outsNeeded):
        self.name = name
        self.cards = cards
        self.chance = chance
        self.outs = outs

   def toString(self):

      outstring = self.name + ": ["
      comma = ""

      for c in self.cards:
         outstring += comma + c.toShortString()
         comma = ","
      outstring += "]"

      return outstring

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