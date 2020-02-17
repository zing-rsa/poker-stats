from Entities.Suits import Suits
from Entities.Card import Card
from Entities.Player import Player
from Entities.Hand import handEnum

class PokerStatter():
    
    visibleCards = []

    allCardsDict = {}
    remainCardsDict = {}
    audienceCards = []

    def getHighestCurrentHand(self):
        return handEnum.default

    def beatsHand(self,hand1,hand2):
        
        

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

        remainCardsDict = self.retrieveRemainingCards(audienceCards)
        
        self.allCardsDict = allCardsDict
        self.remainCardsDict = remainCardsDict
        self.audienceCards = audienceCards

        currentHighestHand = handEnum.default

        for p in players:
            if p.currentHighestHand.value > currentHighestHand.value:
                currentHighestHand = p.currentHighestHand
            

        for p in players:
            p.handsToCheck = self.getHandsToCheck(p, currentHighestHand) # this will need to be filtered by what is above the currentHighestHand
            

        return chancesPerPlayer

    def getHandsToCheck(self, player, currentHighestHand):
        possibleHands = self.getPossibleHands(player)

        handsToCheck = {}

        for h, c in possibleHands:
            if handEnum[h] > handEnum[currentHighestHand]:
                pass
                
        return "test"



    def getPossibleHands(self, player):

        possibleHands = {}

        player.handChances = self.getHandChances(player)

        for h, c in player.handChances.items():
            #Possible outcomes
            # 1 - player hit hand - need to check his currentHighestHand
            # % - some percent chance of player getting that card
            # 0 - player cannot hit 

            if c != 0:
                possibleHands[h] = c

        return possibleHands

    def getHandChances(self, player):

        chancesPerHand = {
            "onePair" : self.chanceOfOnePair(player)
            #handEnum[3] : self.chanceOfTwoPair
            #handEnum[4] : self.chanceOfTrips
            #handEnum[5] : self.chanceOfStraight
            #handEnum[6] : self.chanceOfFlush
            #handEnum[7] : self.chanceOfFullHouse
            #handEnum[8] : self.chanceOfQuads
            #handEnum[9] : self.chanceOfStraightFlush
        }

        return chancesPerHand
    
    def chanceOfOnePair(self, player):

        possibleOnePairs = []
             
        totalChance = 0 

        remainingCardsCount = float(52 - len(self.audienceCards))

        onePairReqirements = self.getOnePairCards(self.allCardsDict[player.Id] + self.allCardsDict["TableCards"])
        
        for pCard in player.cards:
            for reqCard in onePairReqirements:

                if pCard.value == reqCard.value:
                    for c in self.getCardsLeftOfValue(reqCard.value):
                        possibleOnePairs.append({
                            "cards": [pCard, c],
                            "chance": self.chanceOfGettingCard(remainingCardsCount, 1)
                        })

        if len(onePairReqirements) == 0:
            # player has hit one pair
            return 1

        for c in onePairReqirements:
            totalChance += self.chanceOfGettingCard(remainingCardsCount, self.remainCardsDict[c.value])

        return  totalChance
        

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
                elif c.value == v.value:
                    #Found 1 pair - return 0 required cards
                    return []
                    
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
        tempDict = {}

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

    def getFlushCards(self, visibleCards):  
        
       #[{"id":1,"suit": "H", "value": 2},{"id":2,"suit": "C", "value": 4}]

        # I realised today that I coded what you coded for this method in a method called 
        # getRemainingCards which I created while I was doing the one pair chance, so 
        # we could use it for this exact purpose in the future. 
        # But I forgot to show you so yeah.. 

        hearts_count = 0
        diamonds_count = 0
        spades_count = 0
        clubs_count = 0
        
        suitforflush = ""
        
        for card in visibleCards:
            if card.suit == Suits.Hearts:
                hearts_count +=1
            if card.suit == Suits.Diamonds:
                diamonds_count +=1
            if card.suit == Suits.Spades:
                spades_count +=1
            if card.suit == Suits.Clubs:
                clubs_count +=1
        
        if (hearts_count or diamonds_count or spades_count or clubs_count) >=3:# this wont work
            print("The flush is possible")
            
        #suit with higest count to see which cards are needed to completet the flush
        highest = max(hearts_count, diamonds_count, spades_count, clubs_count)
        if hearts_count == highest:
            suitforflush = "hearts"    
        
        if diamonds_count == highest:
            suitforflush = "diamonds"    
        
        if spades_count == highest:
            suitforflush = "spades"    
        
        if clubs_count == highest:
            suitforflush = "clubs"
        
        self.allCardsDict["leftOverCards"]

            
        