class TableSlot():
    
    slotId = -1
    visible = False
    card = None

    def __init__(self, slotId, visible, card):
        self.slotId = slotId
        self.visible = visible
        self.card = card

