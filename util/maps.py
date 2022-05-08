from entities.suits import Suits

value_map = {
    1: 1,
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

hand_scores = {
    "high_card": 0,
    "one_pair": 100,
    "two_pair": 200,
    "trips": 300,
    "straight": 400,
    "flush": 500,
    "full_house": 600,
    "quads": 700,
    "straight_flush": 800,
    "royal_flush": 900,
}
