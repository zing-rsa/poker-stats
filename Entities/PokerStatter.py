from Entities.Suits import Suits
from Entities.Card import Card
from Entities.Player import Player
from Entities.HandEnum import handEnum
from Entities.Hand import Hand
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

        self.getPossibleWinningHands(players)

        for p in players:
                for h in p.possibleWinningHands:
                    p.cumulativeChance += h.chance * 100
                    totalChance += h.chance * 100

                if p.Id == self.currentHighestHandHolder and p.isTied == False:
                    #weight the player with the highest hand
                    p.cumulativeChance += 100
                    totalChance += 100
        
        for p in players:
            if totalChance == 0 or p.cumulativeChance == 0:
                chancesPerPlayer[p.Id] = 0
            else:
                p.relativeChance = p.cumulativeChance / totalChance * 100
                chancesPerPlayer[p.Id] = p.relativeChance
         
        return chancesPerPlayer


    #region Generic hand management 


    #   Populates each player object with a filtered list of winning Hand Objects
    #   Expects:    players - list of player Objects
    #   Returns:    null(assigns by reference to player)
    def getPossibleWinningHands(self, players):

        for p in players:
            p.possibleHands = self.getAllPossibleHands(p)

        self.currentHighestHand = self.getHighestCurrentHand(players)

        self.checkForTie(players)

        for p in players: 
            handsToCheck = []
            for key in p.possibleHands:
                if handEnum[key].value >= handEnum[self.currentHighestHand.name].value:
                    for hand in p.possibleHands[key]:
                        if hand.chance != 0 and self.compareHands(hand, self.currentHighestHand) == 1 and self.checkForOpponentWin(p, players, hand) == False:
                            # need to find a way to check if the result would mean that another player 
                            # would have a higher hand
                            handsToCheck.append(hand)

            p.possibleWinningHands = handsToCheck



    def checkForOpponentWin(self, player, opponents, hand):
        for o in opponents:
            if o.Id != player.Id:
                for key in o.possibleHands:
                    for ohand in o.possibleHands[key]:
                        if len(ohand.outsNeeded) == 1  and ohand.outsNeeded[0].Id == hand.outsNeeded[0].Id and self.compareHands(ohand, hand) == 1:
                            return True
        
        return False

    #   Generates a dictionary of hands
    #   Expects:    player - the player object to use
    #   Returns:    dictionary with hand names as keys, 
    #               and lists of Hand Objects as values
    def getAllPossibleHands(self, player):

        chancesPerHand = {
            "highCard"  : self.getPossibleKickers(player), 
            "onePair"   : self.getPossibleOnePairs(player),
            "twoPair"   : self.getPossibleTwoPairs(player)
        #    "trips"     : self.getPossibleTrips(player)
        #    "straight"  : self.getPossibleStraights(player)
        #    "flush"     : self.getPossibleFlushes(player)
        #    "fullhouse" : self.getPossibleFullHouses(player)
        #    "quads"     : self.getPossibleQuads(player)
        #    "straightFlush" : self.getPossibleStraightFlushes(player)
        }

        return chancesPerHand

    #endregion
    
    #region Specific chance of hand calculation methods 

    #   All methods:
    #   Expect:    player: current player object
    #   Return:    a list of Hand objects

    def getPossibleKickers(self,player):

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

    def getPossibleOnePairs(self, player):

        possibleOnePairs = []

        visibleCards = player.cards + self.allCardsDict["TableCards"]
        
        for pCard in visibleCards:
            for c in self.allCards:
                if pCard.value == c.value and pCard.Id != c.Id: # marking this incase it fucks out, check was: pCard.suit != c.suit
                    possibleOnePairs.append(
                        Hand(
                            name    = "onePair",
                            cards   = [pCard,c],
                            chance  = self.chanceOfCard(player, c.suit, c.value),
                            outsNeeded = [c] 
                        ))
                        
        return possibleOnePairs
    
    def getPossibleTwoPairs(self,player):

        possibleTwoPairs = []

        visibleCards = player.cards + self.allCardsDict["TableCards"]

        for card1 in visibleCards:
            for c1 in self.allCards: 
                if card1.value == c1.value and card1.Id != c1.Id:

                    for card2 in visibleCards:
                        if card2.Id != card1.Id and card2.value != card1.value:
                            for c2 in self.allCards:  
                                if card2.value == c2.value and card2.Id != c2.Id:
                                    possibleTwoPairs.append(
                                            Hand(
                                                name    = "twoPair",
                                                cards   = [card1,c1,card2,c2],
                                                outsNeeded = [c1,c2] 
                                            ))
        return possibleTwoPairs

    #endregion

    #region Comparisons and Highs 


    #   Return the highest hand out of all of the players
    #   Expects: players - list of player objects
    #   Returns: A Hand object containing the cards and name of the highest current hand
    def getHighestCurrentHand(self, players):

        highestHand = Hand("default")

        for p in players:
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
            # same combo, find higher kicker(s)

            # possible here to just find the highest card in the cards lists? 
            # ie. one pair, if the highest card from p1.cards + p2.cards gives you the winner
            # two pair? 
            # trips?
            # straight?
            if hand1.name == "highCard":

                return self.highest(hand1.cards[0].value, hand2.cards[0].value)

            elif hand1.name == "onePair":

                return self.highest(hand1.cards[0].value, hand2.cards[0].value)

            elif hand1.name == "twoPair":
                pass
            elif hand1.name == "trips":
                pass
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

    def checkForTie(self,players):

        tiedPlayers = []

        for p in players:
            # for key in p.possibleHands:
            #     if handEnum[key].value == handEnum[self.currentHighestHand.name].value:
            #         for hand in p.possibleHands[key]:# needs to not check possible hands but currentHighestHand
            if self.compareHands(p.currentHighestHand, self.currentHighestHand) == 0:
                tiedPlayers.append(p.Id)

            if len(tiedPlayers) > 1:
                for i in range(len(tiedPlayers)):
                    players[i].isTied = True
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

    #   Retrieve the percent chance of getting a card with matching parameters
    #   Expects:    player  - the current player object being worked on 
    #               suit    - optional suit enum to match on
    #               value   - optional numeric card value to match on
    #   Returns:    the percent chance of getting a card that matches the supplied criteria
    def chanceOfCard(self, player, suit = None, value = None):
        
        accumulativeChance = 0

        remainingCardsCount = float(52 - len(self.audienceCards))

        otherPlayerCards = []

        for key in self.allCardsDict:
            if key != "TableCards" and key != "leftOverCards" and key != player.Id:
                otherPlayerCards += self.allCardsDict[key]
        
        if suit != None and value != None:
            for c in self.allCardsDict[player.Id]:
                if c.value == value and c.suit == suit:
                    return 1
            for c in self.allCardsDict["TableCards"]:
                if c.value == value and c.suit == suit:
                    return 1
            for c in otherPlayerCards:
                if c.value == value and c.suit == suit:
                    return 0

            for i in range(self.tableCardsLeft):
                accumulativeChance += 1/(remainingCardsCount-i)
            return accumulativeChance

        elif suit == None and value != None:

            for i in range(self.tableCardsLeft):
                accumulativeChance += self.remainCardsDict[value]/(remainingCardsCount-i)
            return accumulativeChance

        elif suit != None and value == None:

            for i in range(self.tableCardsLeft):
                accumulativeChance += self.remainCardsDict[suit.name[0]]/(remainingCardsCount-i)
            return  accumulativeChance
        else:
            return "u knob"

    
    #   Remove the given cardSet from a set of cards and return counts of the rest of the cards
    #   Expects: cardSet - list of Card Objects to exclude
    #   Returns: dictionary where each card value and suit is a key, and values are the amount
    #            of the specific key are left in the deck
    def retrieveRemainingCards(self, cardSet):

        occurencesPerCard = self.getOccurencesPerCard(cardSet)
        remaining = {}
        suits = ["C","H","S","D"]

        for i in range(13):
            if (i+1) in occurencesPerCard:
                remaining[i+1] = 4 - occurencesPerCard[i+1]
            else:
                remaining[i+1] = 4

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
        tempDict = {
            "C": 0,
            "D": 0,
            "S": 0,
            "H": 0
        }

        for c in cardSet:
            suit = c.getSuitShort()
               
            if c.value in tempDict:
                tempDict[c.value] = tempDict[c.value] + 1 
            else:
                tempDict[c.value] = 1

            if suit in tempDict:
                tempDict[suit] = tempDict[suit] + 1
            else:
                 tempDict[suit] = 1

        return tempDict

    #endregion
