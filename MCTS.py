import log as lg
import numpy as np

class Node():
    def __init__(self, state):
        self.state = state
        self.currentPlayer = state.currentPlayer
        self.id = state.id
        #edges will be the list of edges going OUT from this node.
        self.edges = []
        
    def isLeaf(self):
        if len(self.edges) == 0:
            return True
        return False
    
    
#what will initial case for P be? simply just 1/7 a piece?
class Edge():
    def __init__(self, nodeI, nodeO, pred, action):
        self.nodeI = nodeI
        self.nodeO = nodeO
        self.action = action
        #N: number of times edge has been visited.
        #W: number of wins from simulations across this edge
        #Q: the expected value of winning for the current player taking the action given.
        #P: at the moment this is not used. should represent the estimate from the perspective of the 
        #current player the expected value of taking an action. I believe this comes from the NN?
        self.stats = {
            'N': 0,
            'W': 0,
            'Q': 0,
            'P': pred
        }
        

class MCTS():
    def __init__(self, root, cpuct):
        self.root = root
        self.cpuct = cpuct
        self.tree = {}
        
    def addNode(self, node):
        self.tree[node.id] = node
        
    def goToEnd(self):
        currNode = self.root
        done = 0
        val = 0
        pathTaken = []
       
        #note the tree construction is not done within this class. This must be done prior to the
        #tree search of course.
        while not currNode.isLeaf():
            totN = 0
            lg.logger_mcts.info('PLAYER ... %d', currentNode.state.currentPlayer)
            bigQU = -1000000
            #confused on this first part.
            if currNode == self.root:
                a;sldkfj
            else:
                epsilon
                
            for action, edge in currNode.edges:
                totN += edge.stats['N']
                
            #enumerate returns the same list but with an "indexed" first part of the tuple
            for i, action, edge in enumerate(currNode.edges):
                #represents the upper confidence bound for the q value, where
                #the q value is just the expected value of taking a given action.
                U = edge.stats['Q'] + self.cpuct * edge.stats['P'] * np.sqrt(totN)/(1+edge.stats['N'])

                Q = edge.stats['W'] / edge.stats['N']
                
                #some algorithms only maximize U, some algorithms maximize Q + U. Not sure what the diff
                #is and if it is of much importance.
                if Q + U > bigQU:
                    bigQU = Q + U
                    bigEdge = edge
                    bigAction = action
                
            lg.logger_mcts.info('DONE...%d', done)

        
            currNode = bigEdge.nodeO
            pathTaken.append(bigEdge)
            actionTaken.append(bigAction)
            nextState, value, end = currNode.state.takeAction(bigAction)
        return currNode, value, done, pathTaken
            
    def backFill(self, leaf, pathTaken):
        lg.logger.info('%%%%%%%% BEGINNING BACKPROPAGATION:  %%%%%%%%%%')
        loser = leaf.currentPlayer
        
        for edge in pathTaken:
            edge.stats['N'] += 1
            sign = 1
            #if the previous move was made by the winning player, adjust the expected win to be 
            if loser == edge.nodeI.currentPlayer:
                sign = -1
            edge.stats['W'] += sign
            edge.stats['Q'] = edge.stats['W']/edge.stats['N']
            
            lg.info('UPDATING EDGE STATS WIN: %f for player %d .... N = %d , W = %f , Q = %f',
                sign, edge.currentPlayer, edge.stats['N'], edge.stats['W'], edge.stats['Q'])
        