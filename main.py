from entities import Table, Dealer, Card, Pokerstatter
from util import Suits
import time

s = {
    "player_cards":  [
        [Card(8, Suits.Diamonds),  Card(10, Suits.Hearts)],
        [Card(12, Suits.Spades),   Card(10, Suits.Spades)]
    ],
    "table_cards": [
        Card(13, Suits.Spades),
        Card(14, Suits.Spades),
        Card(12, Suits.Diamonds),
        Card(12, Suits.Clubs)
    ]
}

def main():

    t = Table(player_count=len(s['player_cards']))
    d = Dealer()

    d.deal(table=t, seed=s)

    d.flip(t)

    print("\nTable: \n")
    print(t.table_cards_str())

    p = Pokerstatter()

    start = time.time()
    print('\nBegin evaluate:')

    p.evaluate(t)

    end = time.time()
    print(f"Completed in {end - start}s")

    print(t.players_str())

    
if __name__ == '__main__':
    main()
