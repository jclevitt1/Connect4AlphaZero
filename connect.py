import numpy as np
class connect:
    #Some notes on representation:
    #1 is O
    #-1 is X
    #
    
    #Action will be represented by:
    #
    
    def __init__(self):
        self.game_name = 'Connect 4'
        #currentPlayer = 1 means it is O's turn.
        self.currentPlayer = 1
        self.gameState = ConnectState(np.zeros(6, 7))
        self.actionSpace = np.zeros(7,)
        self.pieces = {'1':'X', '0': '-', '-1':'O'}
        self.grid_shape = (6,7)
        self.input_shape = (2,6,7)
        self.state_size = len(self.gameState.binary)
        self.action_size = len(self.actionSpace)
    

        

    def printGame(self, state):
        gameStr = ''
        for i in range(6):
            for j in range(7):
                row = 5 - i
                if (self.board[row][j] == -1):
                    gameStr += 'X'
                elif (self.board[row][j] == 0):
                    gameStr += ' '
                else:
                    gameStr += 'O'
                gameStr += ' | '
            gameStr += '\n'
        print(gameStr)
    
    def reset(self):
        self.gameState = ConnectState(np.zeros(6, 7))
        self.currentPlayer = 1
        return self.
        

    
    #only to be called when the game has already ended. Not putting a check on this because it would be taxing on the computing power.
    
class ConnectState:
    def __init__(self, board, currentPlayer):
        self.board = board
        self.currentPlayer = currentPlayer
        
        self.allowedActions = self._allowedActions()
        self.isEndGame, self.value = self.gameEnded()
        #omitting self.score
        
        self.binary = self.binary()
        self.id = self._convertStateToId()
        
    #######
    # notes on making a move:
    # update the row sum, update the game state
    ######

    #returns a list of numbers representing (in absolute value) the list of valid moves on the connect 4 board
    def getValidActions(self, state):
        toReturn = []
        for i in range(7):
            if (self.validCol(state, i)):
                toReturn.append(i + 1)         
        return toReturn 
    
    def validCol(self, state, col):
        if (abs(self.board[5][col]) == 1):
            return False
        return True

    def nextState(self, col):
        row = self.getRow(state, col)
        newBoard = self.board
        if (row < 6):
            if (state.playerTurn == 1):
                newBoard[row][col] = 1
            else:
                newBoard[row][col] = -1
        else:
            raise ValueError('This is not a valid move.')      
        newState = ConnectState(newBoard, -self.currentPlayer)
        return newState
    
    def getRow(self, state, col):
        for i in range(6):
            if (abs(self.board[5-i][col]) == 1):
                return (5-i) + 1
        return 0
        
    #if the previous player played a winning move, this returns True (or if the board is filled). otherwise,
    #this returns False.
    def gameEnded(self):
        if (sum(abs(state[i][j] for i in range(6) for j in range(7)) == 42):
            return True
        winv, valv = self.checkVertical() 
        winh, valh = self.checkHorizontal() 
        wind, vald = self.checkDiagonal()
        return winv or winh or wind, np.sign(sum(valv, valh, vald))
    
            #all the check methods return a boolean and a value. 
            #the boolean represents whether the game has ended.
            #the value represents which player won the game.
            #since this method should only be called to evaluate if the PREVIOUS player made a winning move,
            #the value should always be == -self.currentPlayer
    def checkHorizontal(self):
        numInRow = 0
        for i in range(6):
            win, val = self.checkHHelper(-self.currentPlayer, i)
            if (win):
                return True, val
        return False, 0
    
    def checkHHelper(self, dv, i):
        #explaination on sheet.    
        if (state[i][3] == dv):
            if (state[i][2] == dv):
                if (state[i][1] == dv):
                    if (state[i][0] == dv):
                        return True, dv
                    elif (state[i][4] == dv):
                        return True, dv
                elif (state[i][4] == dv):
                    if (state[i][5] == dv):
                        return True, dv
            elif (state[i][4] == dv):
                        if (state[i][5] == dv):
                            if (state[i][6] == dv):
                                return True, dv                 
        return False, dv
            
    def checkVertical(self):
        numInCol = 0
        for j in range(7):
            win, val = self.checkVHelper(-self.currentPlayer, j)
            if (win):
                return True, val
        return False, 0
    
    def checkVHelper(self, dv, j):
        #check center 2, then check if there are two pieces around it
        if (self.board[2][j] == dv and self.board[3][j] == dv):
            if (self.board[1][j] == dv):
                if (self.board[0][j] == dv):
                    return True, dv
                elif (self.board[4][j] == dv):
                    return True, dv
            elif (self.board[4][j] == dv):
                if (self.board[5][j] == dv):
                    return True, dv
        return False, 0
                    
                    
    def checkDiagonal(self):
        for i in range(3, 6):
            for j in range(7):
                if (self.board[i][j] == -self.currentPlayer):
                    win, val = self.checkDHelper(i, j, -self.currentPlayer)
                    if (win):
                        return True, val
        return False, 0
    
    def checkDHelper(self, i, j, dv):
        if (j <= 3):
            if (self.board[i-1][j+1] == dv):
                if (self.board[i-2][j+2] == dv):
                    if (self.board[i-3][j+3] == dv):
                        return True, dv
        if (j >= 3):
            if (self.board[i-1][j-1] == dv):
                if (self.board[i-2][j-2] == dv):
                    if (self.board[i-3][j-3] == dv):
                        return True, dv
        return False, 0
