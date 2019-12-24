from Entities.SuitsEnum import Suits
from Entities.Card import Card

testcard =  Card(1, 1, Suits.Hearts)

print(testcard.suit.name)