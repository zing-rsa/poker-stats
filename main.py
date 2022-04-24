from Entities.Table import Table
from Entities.Suits import Suits
from Entities.Card import Card
from Entities.PokerStatter import PokerStatter
from Entities.Hand import Hand
from Entities.Suits import Suits
from Entities.Dealer import Dealer

seed = {
    "playerCards":  [
        [Card(0, 12, Suits.Clubs),Card(1, 11, Suits.Diamonds)],
        [Card(2, 3, Suits.Hearts),Card(3, 4, Suits.Diamonds)]
    ],
    "tableCards": [
        Card(4, 8, Suits.Diamonds),
        Card(5, 6, Suits.Clubs),
        Card(6, 14, Suits.Diamonds),
        Card(7, 2, Suits.Clubs),
        Card(8, 13, Suits.Spades)
    ]
}

t = Table(2)
d = Dealer()

d.deal(t, seed)

print("\nPlayers: \n")
print(t.playersToString())

print("\nTable: \n")
print(t.tableCardsExposedToString())

p = PokerStatter()


