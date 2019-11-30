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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # distance to ghost and minimum distance to food have the same weight
        score=0

        foodList=[]
        for food in newFood.asList():
            foodList.append(manhattanDistance(newPos, food))
        if(foodList)!=[]:
            score+=10/min(foodList)

        for ghost in newGhostStates:
            if manhattanDistance(newPos, ghost.getPosition()) > 0:
                score -= 10/ manhattanDistance(newPos, ghost.getPosition())
            else:
                return -float("inf") #hitting a ghost results in losing of the game so it is the worst move

        return score+successorGameState.getScore() #return the score+ the next score because pacman subs his score by 1 everytime he moves.

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
        """
        "*** YOUR CODE HERE ***"
        def max_value(gameState, depth, pacmanIndex):
            v = ["", -float("inf")]
            if not gameState.getLegalActions(pacmanIndex):  #terminal-test(state)-score of leaves
                v[0]="terminal state"
                v[1]=self.evaluationFunction(gameState)
                return v

            for action in gameState.getLegalActions(pacmanIndex):
                temp=minimax(gameState.generateSuccessor(pacmanIndex, action), depth, pacmanIndex + 1) #goes to min because always after pacman, ghosts play
                if temp[1]>v[1]:
                    v[1]=temp[1]
                    v[0]=action
            return v

        def min_value(gameState, depth, ghostIndex):
            v = ["", float("inf")]

            if not gameState.getLegalActions(ghostIndex): #terminal-test(state)-score of leaves
                v[0] = "terminal state"
                v[1] = self.evaluationFunction(gameState)
                return v

            for action in gameState.getLegalActions(ghostIndex):
                temp= minimax(gameState.generateSuccessor(ghostIndex, action), depth, ghostIndex + 1) #goes to min if next agent is ghost or max if next agent is pacman
                if temp[1] < v[1]:
                    v[1]=temp[1]
                    v[0]=action
            return v

        def minimax(gameState, depth, agentIndex):
            if agentIndex==gameState.getNumAgents(): #if all agents(both pacman and ghosts) have played, then pacman plays again
                depth=depth+1
                agentIndex=0
            if (depth == self.depth): #terminal-reached the end of the tree/depth that was given
                v=["state",self.evaluationFunction(gameState)]
                return v
            elif (agentIndex == 0): #pacman plays
                return max_value(gameState, depth, 0)
            elif (agentIndex > 0): #ghost plays
                return min_value(gameState, depth, agentIndex)

        action = minimax(gameState, 0, 0)
        return action[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_value(gameState, depth, pacmanIndex,a,b):
            v = ["", -float("inf")]
            if not gameState.getLegalActions(pacmanIndex):  #terminal-test(state)-score of leaves
                v[0]="terminal state"
                v[1]=self.evaluationFunction(gameState)
                return v

            for action in gameState.getLegalActions(pacmanIndex):
                temp=minimax(gameState.generateSuccessor(pacmanIndex, action), depth, pacmanIndex + 1,a,b) #goes to min because always after pacman, ghosts play
                if temp[1]>v[1]:
                    v[1]=temp[1]
                    v[0]=action

                if v[1] >b: return v
                a=max(a,v[1])
            return v

        def min_value(gameState, depth, ghostIndex,a,b):
            v = ["", float("inf")]

            if not gameState.getLegalActions(ghostIndex): #terminal-test(state)-score of leaves
                v[0] = "terminal state"
                v[1] = self.evaluationFunction(gameState)
                return v

            for action in gameState.getLegalActions(ghostIndex):
                temp= minimax(gameState.generateSuccessor(ghostIndex, action), depth, ghostIndex + 1,a,b) #goes to min if next agent is ghost or max if next agent is pacman
                if temp[1] < v[1]:
                    v[1]=temp[1]
                    v[0]=action
                if v[1] < a: return v
                b = min(b,v[1])
            return v

        def minimax(gameState, depth, agentIndex,a,b):
            if agentIndex==gameState.getNumAgents(): #if all agents(both pacman and ghosts) have played, then pacman plays again
                depth=depth+1
                agentIndex=0
            if (depth == self.depth): #terminal-reached the end of the tree/depth that was given
                v=["state",self.evaluationFunction(gameState)]
                return v
            elif (agentIndex == 0): #pacman plays
                return max_value(gameState, depth, 0,a,b)
            elif (agentIndex > 0): #ghost plays
                return min_value(gameState, depth, agentIndex,a,b)

        action = minimax(gameState, 0, 0, -float("inf"), float("inf"))
        return action[0]

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
        def max_value(gameState, depth, pacmanIndex):
            v = ["", -float("inf")]
            if not gameState.getLegalActions(pacmanIndex):  #terminal-test(state)-score of leaves
                v[0]="terminal state"
                v[1]=self.evaluationFunction(gameState)
                return v

            for action in gameState.getLegalActions(pacmanIndex):
                temp=expectimax(gameState.generateSuccessor(pacmanIndex, action), depth, pacmanIndex + 1) #goes to min because always after pacman, ghosts play
                if temp[1]>v[1]:
                    v[1]=temp[1]
                    v[0]=action
            return v
        def expect_value(gameState, depth, ghostIndex):
            v = ["", 0]
            if not gameState.getLegalActions(ghostIndex):  # terminal-test(state)-score of leaves
                v[0] = "terminal state"
                v[1] = self.evaluationFunction(gameState)
                return v

            chance = 1.0 / len(gameState.getLegalActions(ghostIndex)) #probality of actions.
            # e.g if a ghost can only get to north and south then we have two options so the probability of choosing one of them is 1/2

            for action in gameState.getLegalActions(ghostIndex):
                temp = expectimax(gameState.generateSuccessor(ghostIndex, action), depth,ghostIndex + 1)  # goes to expect_value if it is a ghost, or max value if it's pacman
                v[1] =v[1]+(temp[1]*chance)
                v[0] = action
            return v
        def expectimax(gameState, depth, agentIndex):
            if agentIndex==gameState.getNumAgents(): #if all agents(both pacman and ghosts) have played, then pacman plays again
                depth=depth+1
                agentIndex=0
            if (depth == self.depth): #terminal-reached the end of the tree/depth that was given
                v=["state",self.evaluationFunction(gameState)]
                return v
            elif (agentIndex == 0): #pacman plays
                return max_value(gameState, depth, 0)
            elif (agentIndex > 0): #ghost plays
                return expect_value(gameState, depth, agentIndex)

        action = expectimax(gameState, 0, 0)
        return action[0]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: We create the score depending on the distances from food and ghosts. Food value is assigned to ten so for the closest food we add to the score value 10 divided by
      the distance of the closest food. If a ghost is scared the value of eating it is 50(very high) so we add to the score 50 divided by the distance of this ghost. Lastly we sub
      from the score value 10 divided by distance to ghost when a ghost is a threat. It is noteworthy that in the end we return the score+ the current score because pacman subs
      his score by 1 everytime he moves.
    """
    "*** YOUR CODE HERE ***"
    score = 0
    #distance to ghost and minimum distance to food have the same weight

    foodList = []
    for food in currentGameState.getFood().asList():
        foodList.append(manhattanDistance(currentGameState.getPacmanPosition(), food))
    if foodList != []:
        score += 10 / min(foodList)

    for ghost in currentGameState.getGhostStates():
        if manhattanDistance(currentGameState.getPacmanPosition(), ghost.getPosition()) > 0:
            if ghost.scaredTimer > 0:
                score += 50 / manhattanDistance(currentGameState.getPacmanPosition(), ghost.getPosition()) #important to eat a scared ghost
            else:
                score -= 10 / manhattanDistance(currentGameState.getPacmanPosition(), ghost.getPosition())
        else: return -float("inf")


    return score+currentGameState.getScore()
# Abbreviation
better = betterEvaluationFunction

