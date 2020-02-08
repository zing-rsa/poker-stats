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

pr.printCards(t.tableCards)

p = PokerStatter()

p.genChancePerPlayer(t.getAllCardsDict(), t.players)





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