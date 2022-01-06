class ConnectState:
    def __init__(self, state, oTurn):
        self.s = state
        self.oTurn = oTurn
        
    def getOTurn(self):
        return self.oTurn