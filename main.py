from Entities.Table import Table
from Entities.Suits import Suits
from Entities.Card import Card

t = Table(2)

t.startNewHand()

print("\nPlayers:", end="\n\n")

t.printPlayers()

print("\nExposed Table:", end="\n\n")

t.printTableCardsExposed()

print("\n1st betting round:", end="\n\n")

t.printTableCards()

print("\n2nd betting round:", end="\n\n")
t.nextBettingRound()
t.printTableCards()

print("\n3rd betting round:", end="\n\n")
t.nextBettingRound()
t.printTableCards()

print("\n4th betting round:", end="\n\n")
t.nextBettingRound()
t.printTableCards()

print("\nFinal bets are placed", end="\n\n")

