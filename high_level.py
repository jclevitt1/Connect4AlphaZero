import numpy as np
def policyIterSP(game, numMCTSSims):
    nnet = initNNet()                                       # initialise random neural network
    examples = []    
    for i in range(numIters):
        for e in range(numEps):
            examples += executeEpisode(game, nnet, numMCTSSims)          # collect examples from this game
        new_nnet = trainNNet(examples)                  
        frac_win = pit(new_nnet, nnet)                      # compare new net with previous net
        if frac_win > threshold: 
            nnet = new_nnet                                 # replace with new net            
    return nnet

def executeEpisode(game, nnet, numMCTSSims):
    examples = []
    s = game.startState()
    mcts = MCTS()                                           # initialise search tree   
    while True:
        for _ in range(numMCTSSims):
            mcts.search(s, game, nnet)
        examples.append([s, mcts.pi(s), None])              # rewards can not be determined yet 
        a = np.random.choice(len(mcts.pi(s)), p=mcts.pi(s))    # sample action from improved policy
        s = game.nextState(s,a)
        if game.gameEnded(s):
            examples = assignRewards(examples, game.gameReward(s)) 
            return examples

        
def assignRewards(examples, outcome):
    for i in range(len(examples)):
        examples[i][2] = outcome
    return examples