
class Hand():
   
   name = "default"
   chance = 0
   cards = []
   outsNeeded = []

   def __init__(self, name = None, cards = None, chance = None, outsNeeded = None):
        if name   is not None: self.name   = name
        if cards  is not None: self.cards  = cards
        if chance is not None: self.chance = chance
        if outsNeeded is not None: self.outsNeeded = outsNeeded