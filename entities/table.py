from entities.player import Player
from entities.card import Card
from util import suitMap


class TableSlot():

    def __init__(self, slotId, visible, card):
        self.slotId = slotId
        self.visible = visible
        self.card = card


class Table():
    players = []
    slots = [None] * 5
    state = "preflop"
    deck = []
    cardsToFlip = 5

    def __init__(self, playerCount):
        for i in range(playerCount):
            p = Player()
            self.players.append(p)

        for i in range(2, 15):
            for j in range(4):
                self.deck.append(Card(i, suitMap[j]))

    def removeFromDeck(self, card):
        idxs = []
        for i, c in enumerate(self.deck):
            if c.suit == card.suit and c.value == card.value:
                self.deck.pop(i)
                break

    def tableCardsExposedToString(self):
        out = ''
        space = ''
        for s in self.slots:
            out = out + space + s.card.str
            space = ' '
        return out

    def tableCardsToString(self):
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

    def playersToString(self):
        out = ''
        newline = ''
        for p in self.players:
            out += newline + '(' + p.toString() + ')'
            out += '\nHands:\n' + p.handsToString()
            newline = '\n'
        return out
