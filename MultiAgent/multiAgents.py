# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import math
from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        "*** YOUR CODE HERE ***"
        score = 999999
        food = currentGameState.getFood().asList()
        if len(newFood) < len(food):
            score += 100

        dotDistance = [util.manhattanDistance(newPos, i) for i in newFood]
        if len(dotDistance) != 0:
            cloestDot = min(dotDistance)
            score -= cloestDot
        else: 
            score += 500

        ghostPos = [gs.getPosition() for gs in newGhostStates]
        for gp in ghostPos:
            pacToGhoDistance = util.manhattanDistance(newPos, gp) 
            if pacToGhoDistance ==  1 or pacToGhoDistance == 0:
                score = 0
        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """


    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"


        def isGameDone(currState):
            return currState.isLose() or currState.isWin()
        
        def minmax(currState, depth, agentId, isMax):
            if isGameDone(currState) or depth == self.depth:
                return self.evaluationFunction(currState)
            actions = currState.getLegalActions(agentId)

            if isMax:
                return max([minmax(currState.generateSuccessor(0, action), depth, 1, False) for action in actions])
            else:
                if agentId == currState.getNumAgents() - 1:
                    return min([minmax(currState.generateSuccessor(agentId, action), depth + 1, 0, True) for action in actions])
                else:
                    return min([minmax(currState.generateSuccessor(agentId, action), depth, agentId + 1, False) for action in actions])
            

        actions = gameState.getLegalActions(0)
        actionsValue = [(minmax(gameState.generateSuccessor(0, action), 0, 1, False), i) for i, action in enumerate(actions)]
        optimalActionId = max(actionsValue)[1]

        return actions[optimalActionId]
        # def maxValue(currState, depth):
        #     if isGameDone(currState) or depth == self.depth:
        #         return self.evaluationFunction(currState)
        #     pacactions = currState.getLegalActions(0)
        #     return max([minValue(currState.generateSuccessor(0, action), depth + 1, 1) for action in pacactions])

        # def minValue(currState, depth, agentId):
        #     if isGameDone(currState):
        #         return self.evaluationFunction(currState)

        #     gsactions = currState.getLegalActions(agentId)
        #     if agentId == currState.getNumAgents() - 1:
        #         return min([maxValue(currState.generateSuccessor(agentId, action), depth) for action in gsactions])
        #     else:
        #         return min([minValue(currState.generateSuccessor(agentId, action), depth, agentId + 1) for action in gsactions])
            
        # actions = gameState.getLegalActions(0)
        # actionsValue = [(minValue(gameState.generateSuccessor(0, action), 1, 1), i) for i, action in enumerate(actions)]
        # optimalActionId = max(actionsValue)[1]

        # return actions[optimalActionId]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def isGameDone(currState):
            return currState.isLose() or currState.isWin()

        def maxValue(state, depth, alpha, beta, agentId):
            if isGameDone(state) or depth == self.depth:
                return self.evaluationFunction(state)

            actions = state.getLegalActions(agentId)
            v = float('-inf')
            for action in actions:
                currV = minValue(state.generateSuccessor(agentId, action), depth, alpha, beta, 1)
                if currV > v:
                    v = currV
                    if depth == 0:
                        returnAction = action
                if v > beta:
                    return v
                alpha = max(alpha, v)
            
            if depth == 0:
                return returnAction
            return v


        def minValue(state, depth, alpha, beta, agentId):
            if isGameDone(state):
                return self.evaluationFunction(state)
            actions = state.getLegalActions(agentId)

            v = float('inf')   
            for action in actions:
                newState = state.generateSuccessor(agentId, action)
                if agentId == state.getNumAgents() - 1:
                    v2 = maxValue(newState, depth + 1, alpha, beta, 0)  
                else:
                    v2 = minValue(newState, depth, alpha, beta, agentId + 1)
                v = min(v, v2)
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v

        optimalAction = maxValue(gameState, 0, float('-inf'), float('inf'), 0)
        return optimalAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        # Detect whether the game is over
        def isGameDone(currState):
            return currState.isLose() or currState.isWin()
        
        # exMax function can find a 
        def expMax(currState, depth, agentId, isMax):
            if isGameDone(currState) or depth == self.depth:
                return self.evaluationFunction(currState)
            actions = currState.getLegalActions(agentId)

            if isMax:
                return max([expMax(currState.generateSuccessor(0, action), depth, 1, False) for action in actions])
            else:
                p = 1.0 / len(actions)
                exp = 0
                for action in actions:
                    newState = currState.generateSuccessor(agentId, action)

                    if agentId == currState.getNumAgents() - 1:
                        exp += expMax(newState, depth + 1, 0, True) * p 
                    else:
                        exp += expMax(newState, depth, agentId + 1, False) * p
            return exp

        actions = gameState.getLegalActions(0)
        actionsValue = [(expMax(gameState.generateSuccessor(0, action), 0, 1, False), i) for i, action in enumerate(actions)]
        optimalActionId = max(actionsValue)[1]

        return actions[optimalActionId]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: In this function, we must let the pacman eact capusle, then 
                 it can eat the monstor to get higher grade. So I set detect 
                the scared time for the monster, if the time > 0 which means 
                the monster can be hunter during this period. And we can try 
                to catch the monster during this period if our dot target does 
                not conflit with our monster
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    pos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    ghostState = currentGameState.getGhostStates()
    score = currentGameState.getScore()
    newScaredTimes = [ghostState.scaredTimer for ghostState in ghostState]
    capsules = currentGameState.getCapsules()
    distanceCapsules = [manhattanDistance(pos, c) for c in capsules]
    scared = 0
    ghostdistance = 0
    scaredDistance = 0 
    dotDistance = [manhattanDistance(pos, i) for i in foodList]
    ghostdistances = [manhattanDistance(pos, gs.getPosition()) for gs in ghostState]

    
    if len(distanceCapsules) == 0:
        closetCapsules = 0
    else:
        closetCapsules = 1.0/min(distanceCapsules) * 50


    if len(dotDistance) != 0:
        cloestDot = min(dotDistance)
    else:
        cloestDot = -1 

    for i in range(len(ghostdistances)):
        if ghostdistances[i] < 1 and newScaredTimes[0] == 0:
            ghostdistance = 800

    if newScaredTimes[0] > 0:
        scared = 200
        ghostdistance = 0
        for i in range(len(ghostdistances)):
            scaredDistance = 1.0/ghostdistances[i] * 200
    foodWeight = 10
    final_score = score + 1.0/cloestDot * foodWeight + scared + scaredDistance - ghostdistance + closetCapsules
    return final_score



# Abbreviation
better = betterEvaluationFunction
