
from entities.suits import Suits
from entities.table import TableSlot
from entities.card import Card

class Dealer():

    def deal(self, table, seed=None):

        if seed is None:
            pass
        else:
            for i, p in enumerate(seed['playerCards']):
                table.players[i].cards[0] = p[0]
                table.players[i].visibleCards.append(p[0])
                table.players[i].cards[1] = p[1]
                table.players[i].visibleCards.append(p[1])
                table.removeFromDeck(p[0])
                table.removeFromDeck(p[1])
            
            for i, c in enumerate(seed['tableCards']):
                table.slots[i] = TableSlot(i, False, c)
    
    def flip(self, table):
        if table.state == "preflop":
            for i in range(3):
                table.slots[i].visible = True
                for p in table.players:
                    p.visibleCards += [table.slots[i].card]
                table.removeFromDeck(table.slots[i].card)
            table.state = "flop"
            table.cardsToFlip = 2
        elif table.state == "flop":
            table.slots[3].visible = True
            for p in table.players:
                p.visibleCards += [table.slots[i].card]
            table.removeFromDeck(table.slots[3].card)
            table.cardsToFlip = 1
            table.state = "turn"
        elif table.state == "turn":
            table.slots[4].visible = True
            for p in table.players:
                    p.visibleCards += [table.slots[i].card]
            table.removeFromDeck(table.slots[4].card)
            table.cardsToFlip = 0
            table.state = "river"