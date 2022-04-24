from Entities.Suits import Suits

def valueMap(value):
    if value <= 10:
        return str(value)
    else:
        return {
            11: "Jack",
            12: "Queen",
            13: "King",
            14: "Ace"
        }[value]

suitMap = {
    0: Suits.Clubs,
    1: Suits.Diamonds,
    2: Suits.Spades,
    3: Suits.Hearts
}