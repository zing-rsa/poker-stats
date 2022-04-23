from Entities.Table import Table
from Entities.Suits import Suits
from Entities.Card import Card
from Entities.PokerStatter import PokerStatter
from Entities.Printer import Printer
from Entities.Hand import Hand
from Entities.Suits import Suits
from Entities.Dealer import Dealer

s = {
    testPlayerCards: [[12,11],[16,31]],
    testTableCards: [12,48,51,4,0]
}

t = Table(2)
d = Dealer()
pr = Printer()

print("\nPlayers:", end="\n\n")
pr.printPlayers(t.players)

print("\nNot Exposed Table:", end="\n\n")
pr.printTableCards(t.tableCards)

print("\nExposed Table:", end="\n\n")
pr.printTableCardsExposed(t.tableCards)

p = PokerStatter()

print("\nChances per Player:", end="\n\n")

#print(p.genChancePerPlayer(t.getAllCardsDict(), t.players))
