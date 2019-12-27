class Printer():

    def printCards(self, cards):
        for c in cards:
            print(c.toString())

    def printTableCards(self, tableCards):
        for c in tableCards:
            if c.visible:
                print(c.toString())
            else:
                print("...")

    def printPlayers(self, players):
        for p in range(len(players)):
            for c in range(2):
                print(f"Player: {p+1}, card({c+1}): {players[p].cards[c].toString()}")

    def printDeck(self, deck):
        for card in deck:
            print(card.toString())

    def printPercentChance(self, chance):
        print("Chance of hitting:" + str(chance) + "%")



