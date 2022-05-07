from entities import Table, Suits, Card, Pokerstatter, Suits, Dealer
import time

s = {
    "playerCards":  [
        [Card(8, Suits.Diamonds),  Card(10, Suits.Hearts)],
        [Card(12, Suits.Spades),   Card(10, Suits.Spades)]
    ],
    "tableCards": [
        Card(13, Suits.Spades),
        Card(14, Suits.Spades),
        Card(12, Suits.Diamonds),
        Card(11, Suits.Hearts),
        Card(13, Suits.Spades)
    ]
}

t = Table(playerCount=2)
d = Dealer()

d.deal(table=t, seed=s)

print("\nTable: \n")
print(t.tableCardsToString())

p = Pokerstatter()

start = time.time()
print('\nBegin evaluate:')

p.evaluate(t)

end = time.time()
print(f"Completed in {end - start}s")

print(t.playersToString())
