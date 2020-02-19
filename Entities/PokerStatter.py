from Entities.Suits import Suits
from Entities.Card import Card
from Entities.Player import Player
from Entities.HandEnum import handEnum
from Entities.Hand import Hand

class PokerStatter():
    
    visibleCards = []
    allCardsDict = {}
    remainCardsDict = {}
    audienceCards = []
    currentHighestHand = Hand("default")

    def getHighestCurrentHand(self, players):

        highestHand = Hand("default")

        for p in players:
            for key in p.handChances:
                for h in p.handChances[key]:
                    if h.chance == 1:

                        testHand = Hand(h.name, h.cards)

                        if self.beatsHand(testHand, highestHand) == 1:
                            highestHand = testHand
        
        return highestHand

    def highest(self, value1, value2):
        if value1 > value2:
            return 1
        elif value1 < value2:
            return 2
        else:
            return 0

    def beatsHand(self,hand1,hand2):

        if handEnum[hand1.name].value > handEnum[hand2.name].value:
            # hand1 is a stronger combo
            return 1
        elif handEnum[hand1.name].value < handEnum[hand2.name].value:
            # hand2 is a stronger combo
            return 2
        else:
            # same combo, find higher kicker(s)
            
            if hand1.name == "onePair":

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


    def beatsHands(self,hand1,hands):
        pass
    
    def genChancePerPlayer(self, allCardsDict, players):

        chancesPerPlayer = {}
        audienceCards = []

        for key in allCardsDict:
            if key == "leftOverCards":
                continue
            audienceCards = audienceCards + allCardsDict[key]
        
        self.allCardsDict = allCardsDict
        self.remainCardsDict = self.retrieveRemainingCards(audienceCards)
        self.occurencesPerCard = self.getOccurencesPerCard(audienceCards) 
        self.audienceCards = audienceCards

        self.getHandsToCheck(players) # this will need to be filtered by what is above the currentHighestHand

        return chancesPerPlayer

    def getHandsToCheck(self, players):
        # returns list of players with hands that could win 

        for p in players:
            p.handChances = self.getHandChances(p)

        self.currentHighestHand = self.getHighestCurrentHand(players)
        

        for p in players: 

            handsToCheck = []

            for key in p.handChances:

                if handEnum[key].value >= handEnum[self.currentHighestHand.name].value:

                    for hand in p.handChances[key]: #all hands(possible or not) better than the currentHighestHand
                        if hand.chance != 0 and self.beatsHand(hand, self.currentHighestHand) == 1:
                            handsToCheck.append(hand)
            
            p.handsToCheck = handsToCheck

    # def getPossibleHands(self, player):

    #     possibleHands = []

        

    #     for h, handChanceList in player.handChances.items():
    #         #Possible outcomes
    #         # 1 - player hit hand - need to check his currentHighestHand
    #         # % - some percent chance of player getting that card
    #         # 0 - player cannot hit 

    #         for handChance in handChanceList:
    #             if handChance.chance != 0:
    #                 possibleHands.append({
    #                     "hand": h,
    #                     "cards": handChance.cards,
    #                     "chance": handChance.chance
    #                 })


    #    return possibleHands

    def getHandChances(self, player):

        chancesPerHand = {
            "onePair" : self.chanceOfOnePair(player)
            #handEnum[3] : self.chanceOfTwoPair
            #handEnum[4] : self.chanceOfTrips
            #handEnum[5] : self.chanceOfStraight
            #"Flush" : self.chanceOfFlush()
            #handEnum[7] : self.chanceOfFullHouse
            #handEnum[8] : self.chanceOfQuads
            #handEnum[9] : self.chanceOfStraightFlush
        }

        return chancesPerHand
    
    def chanceOfOnePair(self, player):

        possibleOnePairs = []

        allCards = []

        for key in self.allCardsDict:
            allCards += self.allCardsDict[key]
        
        for pCard in player.cards:
            for c in allCards:
                if pCard.value == c.value and pCard.suit != c.suit:
                    possibleOnePairs.append(Hand("onePair",[pCard,c],self.chanceOfCard(player, c.suit, c.value)))
                        
        return possibleOnePairs

    def chanceOfCard(self, player, suit = None, value = None):
        
        cardCount = 0
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
            return 1/remainingCardsCount
        elif suit == None and value != None:
            return self.remainCardsDict[value]/remainingCardsCount
        elif suit != None and value == None:
            return  self.remainCardsDict[suit.name[0]]/remainingCardsCount
        else:
            return "u knob"


    def getCardsLeftOfValue(self, value):

        cards = []

        for card in self.allCardsDict["leftOverCards"]:
            if card.value == value:
                cards.append(card)

        return cards


    def getOnePairCards(self,visibleCards):

        cardsOut = []
        
        for c in visibleCards:
            for v in visibleCards:
                if (c.value == v.value) and (c.suit == v.suit):
                    #skip if the same card
                    continue
                # elif c.value == v.value:
                #     #Found 1 pair - return 0 required cards
                #     return []
                    
            cardsOut.append(Card(-1, c.value, Suits.Undefined))
            
        return cardsOut

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

        print("\nRemaining cards: " + str(remaining))

        return remaining

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

    def chanceOfGettingCard(self, cardCount, cardsLeft):
        return float(cardsLeft/cardCount)

    def printVisibleCards(self, visibleCards):
        audienceCards = []
        for card in visibleCards:
            for item in card:
                audienceCards.append(item)
        return audienceCards
