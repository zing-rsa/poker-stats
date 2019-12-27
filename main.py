from Entities.Table import Table
from Entities.Suits import Suits
from Entities.Card import Card
from Entities.PokerStatter import PokerStatter
from Entities.Printer import Printer

t = Table(2)
pr = Printer()

t.startNewHand()

pr.printPlayers(t.players)

print("\nExposed Table:", end="\n\n")

pr.printTableCards(t.tableCards)

for pi in range(len(t.players)):
    p = PokerStatter(t.getVisibleCards(pi))
    print(f"\nCards required for player: {pi} to hit 1 pair", end="\n\n")
    pr.printCards(p.checkFor1Pair())

chance = p.chanceOfOnePair(t.getAudienceVisibleCards())

pr.printPercentChance(chance)


