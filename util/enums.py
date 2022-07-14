import enum


class Hands(enum.Enum):
    high_card = 1
    one_pair = 2
    two_pair = 3
    trips = 4
    straight = 5
    flush = 6
    full_house = 7
    quads = 8
    straight_flush = 9
    royal_flush = 10

class Suits(enum.Enum):
    Hearts = 1
    Spades = 2
    Clubs = 3
    Diamonds = 4
