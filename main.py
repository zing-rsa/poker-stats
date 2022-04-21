from Entities.Table import Table
from Entities.Suits import Suits
from Entities.Card import Card
from Entities.PokerStatter import PokerStatter
from Entities.Printer import Printer
from Entities.Hand import Hand
from Entities.Suits import Suits

#region comments
# for i in range(13):
#     # i = 2 
#     for suit1 in suits:
#         # H                                {2C 2S 2D}
#         pair1Card1 = Card(-1, _suit= suit1 , _value = i+2)
        
#         #2H
#         for suit2 in suits:
#             if suit2 != suit1:

#                 pair1Card2 = Card(-1, _suit = suit2, _value = i+2)
                
#                 # 2S

#                 for j in range(13):
#                     if j != i:
#                         # 3

#                         for suit3 in suits:
#                             # H
#                             pair2Card1 = Card(-1, _suit = suit3, _value = j+2)
                            
#                             # 3H
#                             for suit4 in suits:
#                                 # C
#                                 if suit3 != suit4:
#                                     pair2Card2 = Card(-1,_suit = suit4, _value = j+2)
                                    
#                                     # 3C
#                                     # 
#                                     possibleHand = Hand(
#                                         name = "twoPair",
#                                         cards = [pair1Card1,pair1Card2,pair2Card1,pair2Card2],
#                                         chance = 0.01
#                                     )

#                                     unique = True

#                                     # make the results unique(remove hands where the same cards are used in another order)
#                                     for hand in possibleHands:
#                                        if possibleHand.cards[0] in hand.cards and possibleHand.cards[1] in hand.cards and possibleHand.cards[2] in hand.cards and possibleHand.cards[3] in hand.cards:
#                                            unique = False

#                                     if unique:
#                                         print(possibleHand.toString()) 
#                                         possibleHands.append(possibleHand)

# print("length of hands: " + str(len(possibleHands)))
#endregion
t = Table(2)

testPlayerCards = [[12,11],[16,31]]
testTableCards = [12,48,51,4,0]

t.seed(testPlayerCards,testTableCards)

#t.nextBettingRound()
#t.nextBettingRound()

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
