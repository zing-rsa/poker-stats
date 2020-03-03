from Entities.Table import Table
from Entities.Suits import Suits
from Entities.Card import Card
from Entities.PokerStatter import PokerStatter
from Entities.Printer import Printer
from Entities.Hand import Hand
from Entities.Suits import Suits

# possibleHands = [] 

# suits = [
#     Suits.Clubs,
#     Suits.Hearts,
#     Suits.Spades,
#     Suits.Diamonds
# ]

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

t = Table(2)

testPlayerCards = [[3,16],[20,45]]
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

# Two pair anal-ysis:

# p1 5h 8s

# T 3c 10d 4h ? ?

# if no cards in flop give you pair, 
# then you have to hit both of your hand cards on the turn and river

# one pair in your hand: look for the possible one pairs you could get on the table



# two one pairs from cards in hand: (eg. T = [5c, 8c, 3c, 10D, 12h])

# twoPair: [5H,5C,8S,8H]
# twoPair: [5H,5C,8S,8C]
# twoPair: [5H,5C,8S,8D]

# twoPair: [5H,5D,8S,8H]
# twoPair: [5H,5D,8S,8C]
# twoPair: [5H,5D,8S,8D]

# twoPair: [5H,5S,8S,8H]
# twoPair: [5H,5S,8S,8C]
# twoPair: [5H,5S,8S,8D]


# single one pair from hand and single one pair from table:  (eg. T = [5c, 3c, 3s, 10D, 12h])


# twoPair: [2H,2S:3H,3C]
# twoPair: [2H,2S:3H,3S]
# twoPair: [2H,2S:3H,3D]

# twoPair: [2H,2S:3D,3C]
# twoPair: [2H,2S:3D,3S]
# twoPair: [2H,2S:3D,3H]




# twoPair: [2H,2S:3D,3H
# twoPair: [2H,2S:3D,3C

# twoPair: [2H,2S:3S,3D
# twoPair: [2H,2S:3S,3H
# twoPair: [2H,2S:3S,3C





# twoPair: [5H,5S,2c,2h]
# twoPair: [5H,5S,2c,2d]

# twoPair: [5H,5S,2d,2h]
# twoPair: [5H,5S,2d,2h]
# twoPair: [5H,5S,2d,2h]







# twoPair: [5H,5S, 2s ,52*52]
# twoPair: [5H,5S, 2h ,52*52]
# twoPair: [5H,5S, 2d- 2 ,52*52]
# twoPair: [5H,5S, 52 - 2 ,52*52]
# twoPair: [5H,5S, 52 - 2 ,52*52]
# twoPair: [5H,5S, 52 - 2 ,52*52]

# twoPair: [5H,5C,52,52]
# twoPair: [5H,5D,52,52]

# twoPair: [8S,8H,52,52]
# twoPair: [8S,8D,52,52]
# twoPair: [8S,8C,52,52]

#13  3  12  3
#13*12*3*3 = 1404
#1404/22464 = 6.25%
#3 5's 3 8's
#3/48 * 3/47 * 42/46 * 41/45 * 40/44 * 20 =6.034% 

# we are going to need this
# math.comb(n, k)¶
# Return the number of ways to choose k items from n items without repetition and without order.
# Evaluates to n! / (k! * (n - k)!) when k <= n and evaluates to zero when k > n.
# math.comb(n, k) = n! / (k! * (n-  k)!)