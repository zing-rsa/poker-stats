from entities.hand import Hands, Hand

class Player():

    counter = 0
    
    def __init__(self):
        self.cards = [None] * 2
        self.chance = 0
        self.ties = 0
        self.wins = 0
        self.hands = {
            Hands.royal_flush: 0,
            Hands.straight_flush: 0,
            Hands.quads: 0,
            Hands.full_house: 0,
            Hands.flush: 0,
            Hands.straight: 0,
            Hands.trips: 0,
            Hands.two_pair: 0,
            Hands.one_pair: 0,
            Hands.high_card: 0
        }
        self.id = Player.counter
        Player.counter += 1
    
    def card_str(self):
        return str(self.cards[0].value)+self.cards[0].suit.name[0]+','+str(self.cards[1].value)+self.cards[1].suit.name[0]

    def hand_str(self):
        out = ''
        newline = ''
        for key, val in self.hands.items():
            out += newline + '  ' + key.name + ':' + (" " * (17-len(key.name))) + str(val) + '%'
            newline = '\n'
        return out
