class Printer():

    def printCards(self, cards):
        for c in cards:
            print(c.toString())

    def printTableCards(self, tableCards):
        for s in tableCards:
            if s.visible:
                print(s.card.toString())
            else:
                print("...")

    def printTableCardsExposed(self, tableCards):
        for s in tableCards:
            print(s.card.toString())

    def printPlayers(self, players):
        for p in range(len(players)):
            for c in range(2):
                print(f"Player: {p+1}, card({c+1}): {players[p].cards[c].toString()}")

    def printDeck(self, deck):
        for card in deck:
            print(card.toString())

    def printPercentChance(self, chance):
        print("Chance of hitting:" + str(chance) + "%")



