#this file was taken from a github repository: https://github.com/AppliedDataSciencePartners/DeepReinforcementLearning/blob/master/MCTS.py
#the rest of the files are my own, but I figured implementing MCTS from scratch was not the point of this project.
import numpy as np
import logging
import config

from utils import setup_logger
import loggers as lg

class Node():

    def __init__(self, state):
        self.state = state
        self.playerTurn = state.playerTurn
        self.id = state.id
        self.edges = []

    def isLeaf(self):
        if len(self.edges) > 0:
            return False
        else:
            return True

class Edge():

    def __init__(self, inNode, outNode, prior, action):
        self.id = inNode.state.id + '|' + outNode.state.id
        self.inNode = inNode
        self.outNode = outNode
        self.playerTurn = inNode.state.playerTurn
        self.action = action

        self.stats =  {
                'N': 0,
                'W': 0,
                'Q': 0,
                'P': prior,
                }

class MCTS():

    def __init__(self, root, cpuct):
        self.root = root
        self.tree = {}
        self.cpuct = cpuct
        self.addNode(root)

    def __len__(self):
        return len(self.tree)

    def moveToLeaf(self):

        lg.logger_mcts.info('------MOVING TO LEAF------')

        breadcrumbs = []
        currentNode = self.root

        done = 0
        value = 0

        while not currentNode.isLeaf():

            lg.logger_mcts.info('PLAYER TURN...%d', currentNode.state.playerTurn)
            maxQU = -99999
            
            #if we are in the initial case at the root node
            if currentNode == self.root:
                epsilon = config.EPSILON
                nu = np.random.dirichlet([config.ALPHA] * len(currentNode.edges))
            else:
                epsilon = 0
                nu = [0] * len(currentNode.edges)

            Nb = 0
            for action, edge in currentNode.edges:
                Nb = Nb + edge.stats['N']

            for idx, (action, edge) in enumerate(currentNode.edges):

                U = self.cpuct * \
                    ((1-epsilon) * edge.stats['P'] + epsilon * nu[idx] )  * \
                    np.sqrt(Nb) / (1 + edge.stats['N'])

                Q = edge.stats['Q']

                lg.logger_mcts.info('action: %d (%d)... N = %d, P = %f, nu = %f, adjP = %f, W = %f, Q = %f, U = %f, Q+U = %f'
                , action, action % 7, edge.stats['N'], np.round(edge.stats['P'],6), np.round(nu[idx],6), ((1-epsilon) * edge.stats['P'] + epsilon * nu[idx] )
                    , np.round(edge.stats['W'],6), np.round(Q,6), np.round(U,6), np.round(Q+U,6))

                if Q + U > maxQU:
                    maxQU = Q + U
                    simulationAction = action
                    simulationEdge = edge

            lg.logger_mcts.info('action with highest Q + U...%d', simulationAction)

            newState, value, done = currentNode.state.takeAction(simulationAction) #the value of the newState from the POV of the new playerTurn
            currentNode = simulationEdge.outNode
            breadcrumbs.append(simulationEdge)

        lg.logger_mcts.info('DONE...%d', done)

        return currentNode, value, done, breadcrumbs



    def backFill(self, leaf, value, breadcrumbs):
        lg.logger_mcts.info('------DOING BACKFILL------')

        currentPlayer = leaf.state.playerTurn

        for edge in breadcrumbs:
            playerTurn = edge.playerTurn
            if playerTurn == currentPlayer:
                direction = 1
            else:
                direction = -1

            edge.stats['N'] = edge.stats['N'] + 1
            edge.stats['W'] = edge.stats['W'] + value * direction
            edge.stats['Q'] = edge.stats['W'] / edge.stats['N']

            lg.logger_mcts.info('updating edge with value %f for player %d... N = %d, W = %f, Q = %f'
                , value * direction
                , playerTurn
                , edge.stats['N']
                , edge.stats['W']
                , edge.stats['Q']
                )

            edge.outNode.state.render(lg.logger_mcts)

    def addNode(self, node):
        self.tree[node.id] = node




class MCTS():
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        self.visited = []
        return
    
    def search(state, game, nnet):
        if game.gameEnded(state): return -game.gameReward(state)

        #confused on this "visited" list
        if state not in visited:
            self.visited.add(state)
            #not yet implemented, believe if the neural network is empty this will return 0 for both outputs
            #************************************************
            P[state], v = nnet.predict(state)
            #************************************************
            return -v

        #s has been visited.
        max_u, best_a = -float("inf"), -1
        #change function call validActions
        for action in game.getValidActions(state):
            #Note Q is defined the same in the monte carlo implementation
            #c_puct is defined the same as well.
            #P(s, a) is the intial estimate of taking action a returned by the current neural network 
            #u is simply the upper confidnece bound, what we wish to maximize.
            child_state = game.nextState(action)
            child = None
            childExists = False
            for c in self.children:
                if (child_state == child.state):
                    child = c
                    childExists = True
            if (not childExists):
                child = self.expand(state, action)
                
            allActions = self.getAllActions()
            u = self.q(state, action, child) + c_puct*P[s][a]*sqrt(getAllActions)/(1+child.n())
            #
            if u>max_u:
                max_u = u
                best_a = action
        action = best_a

        sp = game.nextState(state, action)
        v = search(sp, game, nnet)
        
        self.backpropogate(v)

        #Q[s][a] = (N[s][a]*Q[s][a] + v)/(N[s][a]+1)
        #N[s][a] += 1
        return -v
    
    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions
    
    #Redefining: not wins-losses but:
    # (wins-losses)/n for taking action a.
    #Returns expected reward for taking action a.
    #If action has not been taken yet, expand the tree.
    #Q[s][a] notated in the stanford doc.
    def q(self, state, action, child):
        return qHelper(child)
    
    def qHelper(self, child):
        wins = child._results[1]
        loses = child._results[-1]
        return (wins - loses)/(child.n())
    
    def n(self):
        return self._number_of_visits
    
    def expand(self, state, action):
        next_state = self.game.move(action)
        child_node = MonteCarloTreeSearchNode(
        next_state, parent=self, parent_action=action)
        self.children.append(child_node)
        return child_node 
    
    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)
            
    #returns a probability vector of which actions to take.
    #this is one of the "y"
    #should be called after the search function.z
    def pi(self):
        toReturn = [0 for i in range(7)]
        summin = 0
        for child in self.children:
            move = child.parent_action
            toReturn[abs(move)-1] = child.n()
            summin += child.n()
        return [x/summin for x in toReturn]
    
    def getAllActions(self):
        toReturn = 0
        for child in self.children:
            toReturn += child.n()
        return toReturn