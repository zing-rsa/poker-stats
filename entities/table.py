from entities.player import Player
from entities.card import Card
from entities.suits import Suits

class TableSlot():

    def __init__(self, slot_id, visible, card):
        self.slot_id = slot_id
        self.visible = visible
        self.card = card


class Table():
    players = []
    slots = [None] * 5
    state = "preflop"
    deck = []
    cards_to_flip = 5

    def __init__(self, player_count):
        for i in range(player_count):
            p = Player()
            self.players.append(p)

        for i in range(2, 15):
            for j in range(4):
                self.deck.append(Card(i, {0: Suits.Clubs,
                                          1: Suits.Diamonds,
                                          2: Suits.Spades,
                                          3: Suits.Hearts}[j]))

    def remove_from_deck(self, card):
        idxs = []
        for i, c in enumerate(self.deck):
            if c.suit == card.suit and c.value == card.value:
                self.deck.pop(i)
                break

    def table_cards_str(self):
        out = ''
        space = ''
        for s in self.slots:
            if s.visible:
                out = out + space + s.card.str
                space = ' '
            else:
                out = out + space + "[]"
                space = ' '

        return out

    def players_str(self):
        out = ''
        newline = ''
        for p in self.players:
            out += newline + f'\nPlayer: {p.id}  [{p.card_str()}]\nWin: {p.wins}%   |   Tie:{p.ties}%\n          --Hands--\n{str(p.hand_str())}'
            newline = '\n'
        return out
