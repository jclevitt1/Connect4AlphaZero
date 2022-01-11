import numpy as np
class connect:
    #Some notes on representation:
    #1 is O
    #-1 is X
    #
    
    #Action will be represented by:
    #
    
    #omitting the "identities" function listed in the repo.
    
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
    
    #need to edit
    def step(self, action):
        next_state, value, end = self.gameState.takeAction(action)
        self.gameState = next_state
        self.currentPlayer = -self.currentPlayer
        info = None
        return ((next_state, value, end, info))
        

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
        self.id = self.convertStateToId()
        
    #######
    # notes on making a move:
    # update the row sum, update the game state
    ######
    
    def binary(self):
        board1d = self.board.flatten()
        currentPlayer = np.zeros(42)
        currentPlayerBoard[board1d == self.currentPlayer] = 1
        
        otherPlayerBoard = np.zeros(42)
        otherPlayerBoard[board1d == -self.currentPlayer] = -1
        
        return (currentPlayer, otherPlayerBoard)
    
    def convertStateToId(self):
        bothBinary = self.binary[0].append(self.binary[1])
        return ''.join(map(str, bothBinary))
    

    #returns a list of numbers representing (in absolute value) the list of valid moves on the connect 4 board
    def getValidActions(self, state):
        toReturn = []
        for i in range(7):
            if (self.validCol(state, i)):
                toReturn.append(i)         
        return toReturn 
    
    def validCol(self, state, col):
        if (abs(self.board[5][col]) == 1):
            return False
        return True

    #need to add a gameEnded clause of this function.
    def takeAction(self, col):
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
        val = 0
        end = 0
        if newState.isEndGame:
            val = newState.value[0]
            end = 1
        return (newState, newState.value[0], end)
    
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
        winv = self.checkVertical() 
        winh = self.checkHorizontal() 
        wind = self.checkDiagonal()
        end = False
        val = (0, 0)
        if winv or winh or wind:
            end = True
            val = (-1, 1)
        return end, val
    
            #all the check methods return a boolean and a value. 
            #the boolean represents whether the game has ended.
            #the value represents which player won the game.
            #since this method should only be called to evaluate if the PREVIOUS player made a winning move,
            #the value should always be == -self.currentPlayer
    def checkHorizontal(self):
        numInRow = 0
        for i in range(6):
            win = self.checkHHelper(-self.currentPlayer, i)
            if (win):
                return True
        return False, (0, 0)
    
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
                                return True             
        return False
            
    def checkVertical(self):
        numInCol = 0
        for j in range(7):
            win = self.checkVHelper(-self.currentPlayer, j)
            if (win):
                return True
        return False, (0, 0)
    
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
                    return True
        return False
                    
                    
    def checkDiagonal(self):
        for i in range(3, 6):
            for j in range(7):
                if (self.board[i][j] == -self.currentPlayer):
                    win = self.checkDHelper(i, j, -self.currentPlayer)
                    if (win):
                        return True
        return False, (0, 0)
    
    def checkDHelper(self, i, j, dv):
        if (j <= 3):
            if (self.board[i-1][j+1] == dv):
                if (self.board[i-2][j+2] == dv):
                    if (self.board[i-3][j+3] == dv):
                        return True
        if (j >= 3):
            if (self.board[i-1][j-1] == dv):
                if (self.board[i-2][j-2] == dv):
                    if (self.board[i-3][j-3] == dv):
                        return True
        return False
