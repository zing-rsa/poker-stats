
class GameState():

    deck = []
    players = []
    playerCount = len(players)
    tableCards = []
    visibleTableCards = []
    audienceVisibleCards = []
    invisibleCards = []

    def __init__(self, args):

        self.deck = args[0]
        self.players =  args[1]
        self.tableCards = args[2]
        self.visibleTableCards = args[3]
        self.audienceVisibleCards = args[4]
        self.invisibleCards = args[5]