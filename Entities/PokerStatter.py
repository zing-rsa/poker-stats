from Entities.Suits import Suits
from Entities.Card import Card
from Entities.Player import Player
from Entities.HandEnum import handEnum
from Entities.Hand import Hand
from Entities.combination import combination
import math
import pprint


class PokerStatter():

    #region Properties 
    
    visibleCards = []
    allCardsDict = {}
    remainCardsDict = {}
    audienceCards = []
    allCards = []

    tableCardsLeft = 5

    currentHighestHand = Hand("default")
    currentHighestHandHolder = -1

    players = []

    #endregion
    

    #   Return the chance of each player winning the current hand
    #   Expects:    allCardsDict - dictionary with seperate keys for the contained list of Card Objects
    #               players - list of player objects
    #   Returns:    Dictionary of player Id's and their percent chance of winning
    def genChancePerPlayer(self, allCardsDict, players):

        chancesPerPlayer = {}
        audienceCards = []
        totalChance = 0
        playerChance = 0

        for key in allCardsDict:
            self.allCards += allCardsDict[key]

        for key in allCardsDict:
            if key == "leftOverCards":
                continue
            audienceCards = audienceCards + allCardsDict[key]
        
        self.allCardsDict = allCardsDict
        self.remainCardsDict = self.retrieveRemainingCards(audienceCards)
        self.occurencesPerCard = self.getOccurencesPerCard(audienceCards)
        self.audienceCards = audienceCards
        self.tableCardsLeft = 5 - len(allCardsDict["TableCards"])

        self.players = players

        if self.tableCardsLeft == 5:

            for p in self.players:

                preFlopChances = self.getPreFlopChances(p)

                for key in preFlopChances:
                    p.cumulativeChance += preFlopChances[key]

                chancesPerPlayer[p.Id] = p.cumulativeChance * 100

        else:
            self.getPossibleWinningHands()

            for p in self.players:
                for h in p.possibleWinningHands:
                    p.cumulativeChance += h.chance * 100

                    print("Player: " + str(p.Id) + "     hand: " + h.toString()  + "    h.chance: " + str(h.chance) + "    cumulativeChance: " + str(p.cumulativeChance))
                print("\n")

            for p in self.players:
                chancesPerPlayer[p.Id] = p.cumulativeChance * 100
         
        return chancesPerPlayer

    #region Generic hand management 

    #   Populates each player object with a filtered list of winning Hand Objects
    #   Expects:    players - list of player Objects
    #   Returns:    null(assigns by reference to player)
    def getPossibleWinningHands(self):

        for p in self.players:
            p.possibleHands = self.getAllPossibleHands(p)

        self.currentHighestHand = self.getHighestCurrentHand()

        self.checkForTie()

        for p in self.players: 
            handsToCheck = []
            for key in p.possibleHands:
                for hand in p.possibleHands[key]:
                    if hand.chance != 0 and self.compareHands(hand, self.currentHighestHand) == 1 and self.checkForOpponentWin(p, hand) == False:
                        # need to find a way to check if the result would mean that another player 
                        # would have a higher hand
                        handsToCheck.append(hand)

            p.possibleWinningHands = handsToCheck
    
    #endregion

    #region preFlopChances methods

    #   Generates a dictionary of hands
    #   Expects:    player - the player object to use
    #   Returns:    dictionary with hand names as keys, 
    #               and lists of Hand Objects as values
    def getPreFlopChances(self, player):

        chancesPerHand = {
        #    "highCard"  : self.getPossibleKickers(player), 
            "onePair"   : self.onePairPreFlopChance(player)
        #    "twoPair"   : self.twoPreFlopChance(player),
        #    "trips"     : self.tripsPreFlopChance(player)
        #    "straight"  : self.getPossibleStraights(player)
        #    "flush"     : self.getPossibleFlushes(player)
        #    "fullhouse" : self.getPossibleFullHouses(player)
        #    "quads"     : self.getPossibleQuads(player)
        #    "straightFlush" : self.getPossibleStraightFlushes(player)
        }

        return chancesPerHand


    def onePairPreFlopChance(self, player):
        c = combination()
        totalChance = 0

        card1Val = player.cards[0].value
        card2Val = player.cards[1].value
        
        if card1Val == card2Val:
            return 1

        rcc = 52 - len(self.audienceCards)

        #for card in player.cards:
            
        rvc1 = self.remainCardsDict[card1Val]
        rvc2 = self.remainCardsDict[card2Val]

        print('player: ' + str(player.Id))
        print(f"rvc1: {rvc1}, rvc2: {rvc2}, rcc: {rcc}")
        # totalChance of a 1 Pair = P(1st card, not second, no table pair) + P(not 1st card, 2nd card, no table pair) + P(not 1st card, not 2nd, table pair)
        # (3C1 * 11C4 * (4C1 ^ 4) + 3C1 * 11C4 * (4C1 ^ 4) + 11C1 * 4C2 * 10C3 * (4C1 ^ 3)) / (50C5)
        
        totalChance +=  float((c.comb(rvc1, 1) * c.comb(11, 4) * ((c.comb(4,1))^4) + 
                        c.comb(rvc2, 1) * c.comb(11, 4) * ((c.comb(4,1))^4) + 
                        c.comb(11,1) * c.comb(4,2) * c.comb(10,3) * (c.comb(4,1))^3)/(c.comb(rcc,5)))   
        # 3 is number of remaining valued card rvc
            # 11C4 is cimbinations of other 11 cards
            # eg AK
            # rvcA = 3 and rvcK = 3
            # (rvcA * math.comb(13-2,4) + rvcK * math.comb(13-2,4))/(math.comb(50,5))
        print("total chance:", totalChance)
        return totalChance

    def twoPairPreFlopChance(self, player):
        pass

    #endregion

    #region AllPossibleHands methods

    #   Generates a dictionary of hands
    #   Expects:    player - the player object to use
    #   Returns:    dictionary with hand names as keys, 
    #               and lists of Hand Objects as values
    def getAllPossibleHands(self, player):

        chancesPerHand = {
            "highCard"  : self.getPossibleKickers(player), 
            "onePair"   : self.getPossibleOnePairs(player),
            "twoPair"   : self.getPossibleTwoPairs(player),
            "trips"     : self.getPossibleTrips(player),
            "straight"  : self.getPossibleStraights(player),
            "flush"     : self.getPossibleFlushes(player),
            "fullhouse" : self.getPossibleFullHouses(player),
            "quads"     : self.getPossibleQuads(player),
            "straightFlush" : self.getPossibleStraightFlushes(player)
        }

        return chancesPerHand


    def getPossibleKickers(self, player):

        possibleKickers = []

        visibleCards = player.cards + self.allCardsDict["TableCards"]

        for pCard in visibleCards:
            possibleKickers.append(
                Hand(
                    name    = "highCard",
                    cards   = [pCard],
                    chance  = 1
            ))

        return possibleKickers

    def getPossibleOnePairs(self, player): #Possibility for double counting when two pair? 

        possibleOnePairs = []

        for pCard in player.cards:

            for c in player.cards:
                if c.Id != pCard.Id:
                    #get the other card in your hand
                    currentKicker = c

            for c in self.allCards:
                if pCard.value == c.value and pCard.Id != c.Id:

                    possibleHand =  Hand(
                            name    = "onePair",
                            cards   = [pCard,c],
                            outsNeeded = [c],
                            kickers = [currentKicker]
                    )

                    possibleHand.chance = self.getChanceOfOnePair(player.Id, possibleHand)
                    
                    possibleOnePairs.append(possibleHand)
                        
        return possibleOnePairs

    def getPossibleTwoPairs(self,player):
        
        possibleTwoPairs = []

        pCard1 = player.cards[0]
        pCard2 = player.cards[1]

        if pCard1.value == pCard2.value:
            for tCard in self.allCardsDict["TableCards"]:
                
                for card in self.allCards:
                    if card.value == tCard.value and card.suit != tCard.suit:
                        possibleTwoPairs.append(
                            Hand(
                                cards = [pCard1, pCard2, tCard, card],
                                outsNeeded = [card]
                            )
                        )
        else:
            
            pass  



        for pCard in player.cards:
            for tCard in self.allCardsDict["TableCards"]:
                if pCard.value == tCard.value:
                    pass
        return []

        # for c1 in self.allCards:
        #     if c1.value == pCard1.value and c1.Id != pCard1.Id:
        #         for c2 in self.allCards:
        #             if c2.value != c1.value and c2.value == pCard2.value and c2.Id != pCard2.Id:
        #                 hand = Hand(name="twoPair",cards=[pCard1,c1,pCard2,c2],outsNeeded=[c1,c2], chance=0.1)
        #                 print(hand.toString())

        


        #     for c1 in self.allCards: 
        #         if card1.value == c1.value and card1.Id != c1.Id:

        #             for card2 in player.cards:
        #                 if card2.Id != card1.Id and card2.value != card1.value:
        #                     for c2 in self.allCards:
        #                         if card2.value == c2.value and card2.Id != c2.Id:
                                    
        #                             possibleHand = Hand(
        #                                         name    = "twoPair",
        #                                         cards   = [card1,c1,card2,c2],
        #                                         outsNeeded = [c1,c2] 
        #                                     )

        #                             possibleHand.chance = self.chanceOfTwoPair(player, possibleHand)

        #                             #make the results unique(remove hands where the same cards are used in another order)
        #                             unique = True
        #                             for hand in possibleTwoPairs:
        #                                 if possibleHand.cards[0] in hand.cards and possibleHand.cards[1] in hand.cards and possibleHand.cards[2] in hand.cards and possibleHand.cards[3] in hand.cards:
        #                                     unique = False
                                            
        #                             if unique:
        #                                 possibleTwoPairs.append(possibleHand)
                                            
        # for hand in possibleTwoPairs:
        #     print(hand.toString())
        return possibleTwoPairs

    def getPossibleTrips(self, player):

        possibleTrips = []

        for pCard in player.cards:

            for c in player.cards:
                if c.Id != pCard.Id:
                    #get the other card in your hand
                    currentKicker = c

            for c1 in self.allCards:
                if pCard.value == c1.value and pCard.Id != c1.Id:
                    for c2 in self.allCards:
                        if pCard.value == c2.value and pCard.Id != c1.Id and pCard.Id != c2.Id and c1.Id != c2.Id:

                            possibleHand =  Hand(
                                    name = "trips",
                                    cards = [pCard,c1,c2],
                                    outsNeeded = [c1,c2],
                                    kickers = [currentKicker]
                                )

                            possibleHand.chance = self.chanceOfTrips(player.Id, possibleHand)

                            #make the results unique(remove hands where the same cards are used in another order)
                            unique = True
                            for hand in possibleTrips:
                                if possibleHand.cards[0] in hand.cards and possibleHand.cards[1] in hand.cards and possibleHand.cards[2] in hand.cards:
                                    unique = False
                                    
                            if unique:
                                possibleTrips.append(possibleHand)

        return possibleTrips

    def getPossibleFlushes(self,player):
        return []

    def getPossibleStraights(self, player):
        return []

    def getPossibleFullHouses(self,player):
        return []

    def getPossibleQuads(self,player):
        return []

    def getPossibleStraightFlushes(self,player):
        return []

    #endregion

    #region chanceOfHand methods

    #   All methods:
    #   Expect:    player: current player object
    #   Return:    a list of Hand objects
    def getChanceOfOnePair(self, playerId, hand):
        
        visibleCards = self.allCardsDict["TableCards"] + self.allCardsDict[playerId]
        pairValue = hand.outsNeeded[0].value

        self.updateOutsNeeded(playerId, hand)

        if self.opponentHoldsOut(playerId, hand.outsNeeded) or len(hand.outsNeeded) > self.tableCardsLeft:
            return 0
        elif hand.outsNeeded == []:
            if self.getOccurencesPerCard(visibleCards)[pairValue] == 2:
                return 1
            else:
                return 0
        
        rcc = float(52 - len(self.audienceCards))
        rvc = self.remainCardsDict[pairValue] - 1
        
        if self.tableCardsLeft == 1:
            totalChance = (1/rcc)

        elif self.tableCardsLeft == 2:
            totalChance = (1/rcc)*((rcc-1-rvc)/(rcc-1)) * 2

        else:
            totalChance = ((1/rcc) * ((rcc-1-rvc)/(rcc-1)) * ((rcc-2-rvc)/(rcc-2)) * ((rcc-3-rvc)/(rcc-3)) * ((rcc-4-rvc)/(rcc-4)))  * 5
            # formula here is : 1/rcc * rcc-3/rcc-1 * rcc-4/rcc-2 * rcc-5/rcc-3 * rcc-6/rcc-4 - 
            # But need to account for the possibility that another player has gotten a card with the 
            # same value, meaning your chances are lower
            # specfic card, pre flop for !!!one pair!!!
            # rcc (remainingCardCount left in deck, pre flop = 52 - 2n, n = # of players)
            # rvc (remainingValuedCard)

        return totalChance

    def chanceOfTwoPair(self, playerId, hand):
        return 0.01

    def chanceOfTrips(self, playerId, hand):
        #outsNeeded list of cards that are needed to hit teh combination
        #outsNeeded card Objects
        #outsNeeded = [Card1]
        #scenario P1 has 5c => outsNeeded = [5h, 5s]...
        #scenario P1 has 5c, 5d => outsNeeded = [5s]... 
        #if I receive 1 card in outsNeeded, then I need to check that that card does not exist in the opponent(s) hand
        #if I receive 2 cards in outsNeeded, then I still check if it is in the oppenents hand. If that card is in the oppennts hand, then remove that possible hand combination
        
        visibleCards = self.allCardsDict["TableCards"] + self.allCardsDict[playerId]
        tripValue = hand.outsNeeded[0].value

        self.updateOutsNeeded(playerId, hand)

        if self.opponentHoldsOut(playerId, hand.outsNeeded) or len(hand.outsNeeded) > self.tableCardsLeft:
            return 0
        elif hand.outsNeeded == []:
            if self.getOccurencesPerCard(visibleCards)[tripValue] == 3:
                return 1
            else:
                return 0

        rcc = float(52 - len(self.audienceCards))
        rvc = self.remainCardsDict[tripValue] - 1
        if self.tableCardsLeft == 1:
            totalChance = (1/rcc)

        elif self.tableCardsLeft == 2:
            totalChance = (1/rcc)*((rcc-1-rvc)/(rcc-1)) * 2

        else:
            totalChance = ((1/rcc) * ((rcc-1-rvc)/(rcc-1)) * ((rcc-2-rvc)/(rcc-2)) * ((rcc-3-rvc)/(rcc-3)) * ((rcc-4-rvc)/(rcc-4)))  * 5

        return 0.0000001

    #endregion

    #region Comparisons and Highs 


    #   Return the highest hand out of all of the players
    #   Expects: players - list of player objects
    #   Returns: A Hand object containing the cards and name of the highest current hand
    def getHighestCurrentHand(self):

        highestHand = Hand("default")

        for p in self.players:
            for key in p.possibleHands:
                for h in p.possibleHands[key]:
                    if h.chance == 1:

                        testHand = Hand(h.name, h.cards)

                        winningHand = self.compareHands(testHand, highestHand)
                        winningHandPlayer = self.compareHands(testHand, p.currentHighestHand)

                        if winningHand == 1:
                            highestHand = testHand
                            self.currentHighestHandHolder = p.Id
                        if winningHandPlayer == 1:
                            p.currentHighestHand = testHand

        
        return highestHand


    #   Determines which hand from 2 given hands will win
    #   Expects: hand1 - first compare Hand Object 
    #            hand2 - second compare Hand Object
    #   Returns: Numeric representation of which hand won (1 or 2, or 0 if draw)
    def compareHands(self,hand1,hand2):

        if handEnum[hand1.name].value > handEnum[hand2.name].value:
            return 1
        elif handEnum[hand1.name].value < handEnum[hand2.name].value:
            return 2
        else:
            # same combo, find higher value

            if hand1.name == "highCard":
                return self.highest(hand1.cards[0].value, hand2.cards[0].value)

            elif hand1.name == "onePair":
                #need to implement kicker checking
                # if self.highest(hand1.cards[0].value, hand2.cards[0].value) == 0:
                    # return self.highest(hand1.kickers[0], hand2.kickers[0])
                # else:
                return self.highest(hand1.cards[0].value, hand2.cards[0].value)
                

            elif hand1.name == "twoPair":
                pass


            elif hand1.name == "trips":
                #need to implement kicker checking
                # if self.highest(hand1.cards[0].value, hand2.cards[0].value) == 0:
                #     return self.highest(hand1.kickers[0], hand2.kickers[0])
                # else:
                return self.highest(hand1.cards[0].value, hand2.cards[0].value)

            elif hand1.name == "straight":
                pass
            elif hand1.name == "flush":
                pass
            elif hand1.name == "fullHouse":
                pass
            elif hand1.name == "quads":
                pass
            elif hand1.name == "straightflush":
                pass

    def checkForTie(self):

        tiedPlayers = []

        for p in self.players:
            # for key in p.possibleHands:
            #     if handEnum[key].value == handEnum[self.currentHighestHand.name].value:
            #         for hand in p.possibleHands[key]:# needs to not check possible hands but currentHighestHand
            if self.compareHands(p.currentHighestHand, self.currentHighestHand) == 0:
                tiedPlayers.append(p.Id)

            if len(tiedPlayers) > 1:
                for i in range(len(tiedPlayers)):
                    self.players[i].isTied = True
            # this runs for every Jack one pair in his hand
            # try running only through the p.currentHighestHand

    def highest(self, value1, value2):
        if value1 > value2:
            return 1
        elif value1 < value2:
            return 2
        else:
            return 0

    def beatsHands(self,hand1,hands):
        pass

    #endregion

    #region Card utilities 
    
    #   Remove the given cardSet from a set of cards and return counts of the rest of the cards
    #   Expects: cardSet - list of Card Objects to exclude
    #   Returns: dictionary where each card value and suit is a key, and values are the amount
    #            of the specific key are left in the deck
    def retrieveRemainingCards(self, cardSet):

        occurencesPerCard = self.getOccurencesPerCard(cardSet)
        remaining = {}
        suits = ["C","H","S","D"]

        for i in range(13):
            if (i+2) in occurencesPerCard:
                remaining[i+2] = 4 - occurencesPerCard[i+2]
            else:
                remaining[i+2] = 4

        for s in suits:
            if s in occurencesPerCard:
                remaining[s] = 13 - occurencesPerCard[s]
            else:
                remaining[s] = 13

        return remaining


    #   Create totals for how many of each card value and suit exist inside a given cardSet
    #   Expects:    cardSet - list of Card objects to tally up
    #   Returns:    dictionary where each card value and suit is a key, and values are the amount
    #               of the specific key exist in the card set
    def getOccurencesPerCard(self, cardSet):
        occurrenceDict = {
            "C": 0,"D": 0,"S": 0,"H": 0,
            2: 0, 3: 0, 4: 0, 5: 0, 6: 0,
            7: 0, 8: 0, 9: 0, 10: 0,
            11: 0, 12: 0, 13: 0, 14: 0
        }

        for c in cardSet:
            suit = c.getSuitShort()
               
            if c.value in occurrenceDict:
                occurrenceDict[c.value] = occurrenceDict[c.value] + 1 
            else:
                occurrenceDict[c.value] = 1

            if suit in occurrenceDict:
                occurrenceDict[suit] = occurrenceDict[suit] + 1
            else:
                 occurrenceDict[suit] = 1

        return occurrenceDict

    def updateOutsNeeded(self, playerId, hand):

        outsLeft = []

        for out in hand.outsNeeded:
            if out not in self.allCardsDict["TableCards"] and out not in self.allCardsDict[playerId]:
                outsLeft.append(out)

        hand.outsNeeded = outsLeft

    def opponentHoldsOut(self, playerId, outs):

         for out in outs:#gets card in outsNeeded
            for opponent in self.players:#tests for each opponent
                if opponent.Id != playerId:#checking to see that the opponent is not that player
                    for opCard in opponent.cards:#runs through all of the oppenents cards
                        if opCard.Id == out.Id:#check to see if the cards are the same
                           #opponent holds one card, 0% chance of hitting hand
                            return 0
    
    def checkForOpponentWin(self, player, hand):
        for opponent in self.players:
            if opponent.Id != player.Id:
                for key in opponent.possibleHands:
                    for ohand in opponent.possibleHands[key]:
                        if len(ohand.outsNeeded) == 1  and ohand.outsNeeded[0].Id == hand.outsNeeded[0].Id and self.compareHands(ohand, hand) == 1:
                            return True
        
        return False

    #endregion
