# poker-stats
Real-time calculation of the statistical chance of each player in a poker game winning a given hand.

# Usage
No cli yet, you can run test cases by editing `main.py`:
```python
# ...

# The seed state of the table and players.
# - player_cards requires one entry in the player_cards list for each player, with exactly two cards each
# - table_cards requires a list of known cards on the table. This reflects the current state of 
#   the table, so it can be a list with 0 cards, or 3/4/5 cards.
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

    # initialize table state
    t = Table(player_count=len(s['player_cards']))
    d = Dealer()
    d.deal(table=t, seed=s)

    # the dealer can update state to reveal new random cards if necessary
    d.flip(t)

    print("\nTable: \n")
    print(t.table_cards_str())
    
    # initialize the stats engine
    p = Pokerstatter()

    start = time.time()
    print('\nBegin evaluate:')
    
    # evaluate the current table state
    # any valid table state can be evaluated(0 cards or 3/4/5 cards)
    # less known cards takes more time
    p.evaluate(t)

    end = time.time()
    print(f"Completed in {end - start}s")

    print(t.players_str())
# ...
```
