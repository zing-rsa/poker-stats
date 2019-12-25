
class GameState():

    deck = []
    players = []
    playerCount = len(players)
    tableCards = []
    visibleTableCards = []
    audienceVisibleCards = []
    invisibleCards = []

    def __init__(self, _deck, _players, _tableCards, _visibleTableCards, _audienceVisibleCards, _invisibleCards):

        self.deck = _deck
        self.players =  _players
        self.tableCards = _tableCards
        self.visibleTableCards = _visibleTableCards
        self.audienceVisibleCards = _audienceVisibleCards
        self.invisibleCards = _invisibleCards