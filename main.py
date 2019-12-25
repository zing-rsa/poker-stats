import sys
sys.path.append('/Entities/')
from Entities.SuitsEnum import Suits
from Entities.Card import Card
from Entities.Dealer import Dealer
from Entities.GameState import GameState

testcard = Card(1, 1, Suits.Hearts)

print(testcard.toString())

gs = GameState([[],[],[],[],[],[]])

d = Dealer(gs)

d.generateDeck()

d.printDeck()

