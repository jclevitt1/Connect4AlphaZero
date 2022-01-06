#the purposes of making this its own script is simply to lower the memory allocation of each object of connect.

    #######
def printGame(self):
    gameStr = ''
    state = self.game_state
    for i in range(6):
        for j in range(7):
            row = 5 - i
            if (state[row][j] == -1):
                gameStr += 'X'
            elif (state[row][j] == 0):
                gameStr += ' '
            else:
                gameStr += 'O'
        gameStr += ' | '
        gameStr += '\n'
    print(gameStr)