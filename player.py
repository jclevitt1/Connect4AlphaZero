import log as lg
import MCTS as m
from connect import ConnectState as cs
from connect import connect
import numpy as np
import config

class Player():
    #total actions should always be seven, but abstracting this away for the purpose
    #of using this code for other games.
    def __init__(self, name, stateSize, actionSize, simNo, cpuct, model):
        self.name = name
        self.numSims = simNo
        self.cpuct = cpuct
        self.model = model
        
        self.stateSize = stateSize
        self.totalActions = actionSize
        
        self.mcts = None
        
    def newMCTS(self, state):
        lg.logger_mcts.info('%%%%%%%% NEW MCTS TREE FOR PLAYER %s %%%%%%%%%', self.name)
        self.root = m.Node(state)
        self.mcts = m.MCTS(self.root, config.CPUCT)
        
        
    def modelPredict(self, modelInput):
        return self.model.predict(modelInput)
    
    def chooseAction(self, pi, expVal):
        action = np.random.multinomial(1, pi)
        expVal = expVal[action]
        return action, expVal
    
    def getPiAndEV(self):
        pi = np.zeros(self.totalActions, dtype = np.integer)
        expVal = np.zeros(self.totalActions, dtype = np.float32)
        
        totN = 0
        
        for action, edge in self.mcts.root.edges:
            totN += edge.stats['N']
        
        for action, edge in self.mcts.root.edges:
            pi[action] = edge.stats['N']/totN
            expVal[action] = edge.stats['Q']
        return pi, expVal
    
    #performs MCTS simulations equal to the number originally set when this object was setup. 
    def act(self, state):
        if self.mcts is None or state.id not in self.mcts.tree:
            self.newMCTS(state)
        else:
            self.changeRoot(state)
            
        for simulation in range(self.numSims):
            lg.logger_mcts.info('%%%%%%%%%%%%%%%%%%%%%')
            lg.logger_mcts.info('%%SIMULATION NO. %d %', simulation+1)
            lg.logger_mcts.info('%%%%%%%%%%%%%%%%%%%%%')
            self.simulate()
            
        pi, expVal = self.getPiandEV()
        
        action, value = self.chooseAction(pi, expVal)
        
        nextState, endVal, done = self.state.takeAction(action)
        
        neuralValue = -self.neuralPredicts(nextState)
        
        lg.logger_mcts.info('PI VALUES : %s', pi)
        lg.logger_mcts.info('ACTION CHOSEN : %d', action)
        lg.logger_mcts.info('MCTS Q VALUE OF ACTION : %f', value)
        lg.logger_mcts.info('NEURAL PERCEIVED VALUE : %f', neuralValue)
        
        return (action, pi, value, neuralValue)
    
    def simulate(self):
        lg.logger_mcts.info('######### ROOT NODE %s #########', self.mcts.root.state.id)
        lg.logger_mcts.info('######### PLAYER %d    #########', self.mcts.root.currentPlayer)
        #get to end of tree so far.
        leaf, value, done, pathTaken = self.mcts.goToEnd()
        #expand the tree, given the game is not over.
        value, pathTaken = self.expandTree(leaf, value, done, pathTaken)
         #backpropogate.
        self.mcts.backFill(leaf, pathTaken)
        
    def expandTree(self, leaf, value, done, pathTaken):
        lg.logger_mcts.info('********* EXPANDING TREE *********')
        if done == 0:
            neuralValue, neuralProbs, _ = self.neuralPredicts(leaf.state)
            allowedActions = leaf.state.getAllowedActions()
            
            lg.logger_mcts.info('NEURAL PREDICTED VALUE FOR %d : %f', leaf.state.currentPlayer, neuralValue)
            
            for i, action in enumerate(allowedActions):
                nextState, val, end = leaf.state.takeAction(action)
                if nextState.id not in self.mcts.tree:
                    newNode = m.Node(nextState)
                    self.mcts.addNode(newNode)
                    lg.logger_mcts.info('ADDED THE NODE: %s', newNode.id)
                else:
                    #intuition tells me this if case should never be ran.
                    newNode = self.mcts.tree[nextState.id]
                    lg.logger_mcts.info('NODE EXISTED: %s', newNode.id)
                    
                #why are we adding the edge in both the above cases? shouldn't it be simply to the first case?
                #i.e. my intuition tells me this should only be in the first if case above and not apply to the else case. This code has it applicable to both cases.
                newEdge = m.Edge(leaf, newNode, neuralProbs[i], action)
                leaf.edges.append((action, newEdge))
        else:
            lg.logger_mcts.info('GAME ENDED. VALUE FOR %d: %f', leaf.currentPlayer, value)
        return (value, pathTaken)
            
        
    #neuralPredicts not complete yet!!!
    def neuralPredicts(self, state):
        modelIn = np.array([self.model.makeValidModelInput(state)])
        
        
        predictions = self.model.predict(modelIn)
        
        expValNN = predictions[0]
        logitsArr = predictions[1]
        
        expValNN = expValNN[0]
        logitsArr = logitsArr[0]
        
        print(' EXP VAL NN:')
        print(expValNN)
        
        print(' LOGITS ARR NN:')
        print(logitsArr)
        if logitsArr[0] == logitsArr[0]:
            probs = np.exp(logitsArr)
            probs = probs / np.sum(probs)
        else:
            probs = [1/7 for i in range(7)]
        
        allowedActions = state.allowedActions
        
        return ((expValNN, probs, allowedActions))
        
    
    
    def changeRoot(self, state):
        lg.logger_mcts.info('%%%%%%% CHANGING ROOT OF MCTS TO %s FOR PLAYER %s %%%%%%%%%', state.id, self.name)
        self.mcts.root = self.mcts.tree[state.id]
    