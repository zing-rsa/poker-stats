from entities.suits import Suits

valueMap = {
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: "Jack",
    12: "Queen",
    13: "King",
    14: "Ace"
}

suitMap = {
    0: Suits.Clubs,
    1: Suits.Diamonds,
    2: Suits.Spades,
    3: Suits.Hearts
}

handScores = { 
    "highCard": 0,
    "onePair": 100,
    "twoPair": 200,
    "trips": 300,
    "straight": 400,
    "flush": 500,
    "fullHouse": 600,
    "quads": 700,
    "straightFlush": 800
}   