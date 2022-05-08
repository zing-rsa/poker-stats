
from entities.table import TableSlot


class Dealer():

    def deal(self, table, seed=None):

        if seed is None:
            pass
        else:
            for i, p in enumerate(seed['player_cards']):
                table.players[i].cards[0] = p[0]
                table.players[i].cards[1] = p[1]
                table.remove_from_deck(p[0])
                table.remove_from_deck(p[1])

            for i, c in enumerate(seed['table_cards']):
                table.slots[i] = TableSlot(i, False, c)

    def flip(self, table):
        if table.state == "preflop":
            for i in range(3):
                table.slots[i].visible = True
                table.remove_from_deck(table.slots[i].card)
            table.state = "flop"
            table.cards_to_flip = 2
        elif table.state == "flop":
            table.slots[3].visible = True
            table.remove_from_deck(table.slots[3].card)
            table.cards_to_flip = 1
            table.state = "turn"
        elif table.state == "turn":
            table.slots[4].visible = True
            table.remove_from_deck(table.slots[4].card)
            table.cards_to_flip = 0
            table.state = "river"
