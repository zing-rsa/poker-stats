from Entities.Table import Table
from Entities.Suits import Suits
from Entities.Card import Card
from Entities.PokerStatter import PokerStatter
from Entities.Printer import Printer

t = Table(2)

testPlayerCards = [[12,24],[25,36]]
testTableCards = [10,1,2,3,4]

t.seed(testPlayerCards,testTableCards)

t.nextBettingRound()
t.nextBettingRound()

pr = Printer()

print("\nPlayers:", end="\n\n")

pr.printPlayers(t.players)

print("\nNot Exposed Table:", end="\n\n")

pr.printTableCards(t.tableCards)

print("\nExposed Table:", end="\n\n")

pr.printTableCardsExposed(t.tableCards)



p = PokerStatter()

print("\nChances per Player:", end="\n\n")

print(p.genChancePerPlayer(t.getAllCardsDict(), t.players))





#chancesPerPlayer = 

#for key in chancesPerPlayer:
#    print(f"Player: {key} has {chancesPerPlayer[key]}% chance of winning")


#for pi in range(len(t.players)):

#    p = PokerStatter(t.getVisibleCards(pi))

#chance = p.chanceOfOnePair(t.getAudienceVisibleCards())
#print(f"\nChance of player {pi+1} getting 1 pair: {pr.printPercentChance(chance)}")
# chanceOfOnePair
# {"playerOneCards": [,]}
# {"plasydfsfsdf", [,]}
# ....
# {"tableCards": [,,,,]}


# P1 

# one = 100
# two = 0
# trips = 4.5   
# str = 0
# flush 0
# fullhouse 0
# quds 0
# strflush 0

# 9

# P2

# one 100
# two = 0
# trips = 100
# str = 0
# flush = 0
# fullhouse = 0
# quds = 2.3
# strflush = 0


# 4.5/102.3


# P1
# AH 3D
# AD AS AC 3H 3C 3S


# [AH,AD]
# 2.0000228283%

# [AH,AS]
# 2.0000228283%






# P2 
# 4 6

# TableCards
# none
# flop
# turn
# river



