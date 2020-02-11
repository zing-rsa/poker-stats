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

p = PokerStatter()

p.genChancePerPlayer(t.getAllCardsDict(), t.players)



        # {

        #     "p1": [{"h","1"}, {"c","4"}],
        #     "p2": [{"h","1"}, {"c","4"}],
        #     "table": [{"h","1"}, {"c","4"},{"h","1"}, {"c","4"},{"h","1"}]
        #     "leftout" 
        # }











# P1

# one pair = 15%
# two pair = 10%
# trips 10%
# straight 3%

# 26

# P2

# one pair 15%
# two pair 10%
# straight 5%

# 30%









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
