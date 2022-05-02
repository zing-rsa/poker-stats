from entities import Table, Suits, Card, Pokerstatter, Suits, Dealer
import time

s = {
    "playerCards":  [
        [Card(2, Suits.Diamonds),Card(12, Suits.Diamonds)],
        [Card(3, Suits.Hearts),Card(4, Suits.Clubs)]
    ],
    "tableCards": [
        Card(12, Suits.Clubs),
        Card(6, Suits.Clubs),
        Card(14, Suits.Diamonds),
        Card(2, Suits.Clubs),
        Card(13, Suits.Spades)
    ]
}

t = Table(playerCount=2)
d = Dealer()

d.deal(table=t, seed=s)

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


