from Entities.Suits import Suits
from Entities.Card import Card
from Entities.Player import Player
import pprint

class PokerStatter():
    
    visibleCards = []
    
    def genChancePerPlayer(self, allCardsDict, playerCount):

        chancesPerPlayer = {}

        for pi in range(playerCount):
            chancesPerPlayer[pi] = self.chanceOfOnePair(allCardsDict, pi)
        
        return chancesPerPlayer

    
    def chanceOfOnePair(self, allCardsDict, playerId):
                              
        totalChance = 0 

        audienceCards = []

        for key in allCardsDict:
            audienceCards = audienceCards + allCardsDict[key]

        remainCardsDict = self.retrieveRemainingCards(audienceCards)

        remainingCardsCount = float(52 - len(audienceCards))

        onePairReqirementsForPlayer = self.genRequiredCards(allCardsDict["TableCards"] + allCardsDict[playerId])

        for c in onePairReqirementsForPlayer:
            totalChance += self.chanceOfGettingCard(remainingCardsCount, remainCardsDict[c.value])

        return  totalChance
        
    def retrieveRemainingCards(self, visibleCards):
        occurencesPerCard = self.getOccurencesPerCard(visibleCards)
        remaining = {}

        for i in range(13):
            if (i+1) in occurencesPerCard:
                remaining[i+1] = 4 - occurencesPerCard[i+1]
            else:
                remaining[i+1] = 4

        pprint.pprint(remaining)
        return remaining

    def getOccurencesPerCard(self, visibleCards):
        tempDict = {}

        for c in visibleCards:
            if c.value in tempDict:
                tempDict[c.value] = tempDict[c.value] + 1 
            else:
                tempDict[c.value] = 1
                
        pprint.pprint(tempDict)

        return tempDict

    def chanceOfGettingCard(self, cardCount, cardsLeft):
        return float(cardsLeft/cardCount)

    def genRequiredCards(self, visibleCards):

        _onePairReq = self.checkFor1Pair(visibleCards)

        return _onePairReq

    def checkFor1Pair(self,visibleCards):

        cardsOut = []
        
        for c in visibleCards:
            for v in visibleCards:
                if (c.value == v.value) and (c.suit == v.suit):
                    continue
                elif c.value == v.value:
                    return []
                    
            cardsOut.append(Card(-1, c.value, Suits.Undefined))

        return cardsOut

        # do this line per player
        # only pass in cards for each player at a time
        # do this by passing in a dict to this method, that contains 
        # player 1 cards, players2 cards, and all table cards. Then use 
        # that to pass player ones visible cards to the method to determind 
        # his potention chance of getting what he needs
