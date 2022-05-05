from entities import Table, Suits, Card, Pokerstatter, Suits, Dealer
import time

s = {
    "playerCards":  [
        [Card(10, Suits.Diamonds),  Card(11, Suits.Diamonds)],
        [Card(2, Suits.Clubs),   Card(3, Suits.Clubs)]
    ],
    "tableCards": [
        Card(12, Suits.Diamonds),
        Card(13, Suits.Diamonds),
        Card(6, Suits.Diamonds),
        Card(4, Suits.Hearts),
        Card(13, Suits.Spades)
    ]
}

t = Table(playerCount=2)
d = Dealer()

d.deal(table=t, seed=s)

d.flip(t)
d.flip(t)

print("\nPlayers: \n")
print(t.playersToString())

print("\nTable: \n")
print(t.tableCardsToString())

p = Pokerstatter()

start = time.time()
print('\nBegin evaluate:')

p.evaluate(t)

end = time.time()
print(f"Completed in {end - start}s")

print("\nPlayers: \n")
print(t.playersToString())


