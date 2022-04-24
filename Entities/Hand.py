
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