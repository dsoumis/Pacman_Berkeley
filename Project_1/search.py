# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    frontier = util.Stack()
    # The frontier has the nodes and the actions to get to them.
    # The first action is [] because we don't need any movement for the initial state.
    actions = []
    frontier.push([problem.getStartState(), actions])
    explored_set = set()
    while 1:
        if frontier.isEmpty():
            return []  # Failure
        leaf, actions = frontier.pop()
        if problem.isGoalState(leaf):
            return actions
        explored_set.add(leaf)
        succ = problem.getSuccessors(leaf)
        for node in succ:
            # Succ retunrs 3 values. Node 0 are the successor.
            # Node 1 is the action to get to the successor. Node 2 is the cost to it.
            if node[0] not in explored_set and node[0] not in (item[0] for item in frontier.list):
                # We push in the stack the successor
                # and the actions which were needed to get to the parent+ the action to successor
                frontier.push([node[0], actions+[node[1]]])




def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    # BFS differs from dfs in  implementation as shown in slides "Anazitisi se grafous" page 11 and page 27
    node = problem.getStartState()
    path_cost = []
    if problem.isGoalState(node):
        return path_cost
    frontier = util.Queue()
    frontier.push([node, path_cost])
    explored_set = []  # The explored_set is changed from set() to list because it wouldn't work with cornerns problem.
    while 1:
        if frontier.isEmpty():
            return []  # Failure
        node, path_cost = frontier.pop()
        explored_set.append(node)
        succ = problem.getSuccessors(node)
        for child in succ:
            if child[0] not in explored_set and child[0] not in (item[0] for item in frontier.list):
                if problem.isGoalState(child[0]):
                    return path_cost+[child[1]]
                frontier.push([child[0], path_cost+[child[1]]])

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # "Anazitisi se grafous" page 35
    node = problem.getStartState()
    path = []
    frontier = util.PriorityQueue()
    frontier.push([node, path], 0)
    explored_set = set()
    while 1:
        if frontier.isEmpty():
            return []  # Failure
        node, path = frontier.pop()
        if problem.isGoalState(node):
            return path
        explored_set.add(node)
        succ = problem.getSuccessors(node)
        for child in succ:
            if child[0] not in explored_set and child[0] not in (item[2][0] for item in frontier.heap):
                # We call it as item[2][0] because in the heap although we call it as push(item,priority)
                # it is saved as priority,item.

                # The cost of actions (which are the actions of path till the parent + the action to the child)
                # are the priority in priority Queue
                frontier.push([child[0], path+[child[1]]], problem.getCostOfActions(path+[child[1]]))
            elif child[0] in (item[2][0] for item in frontier.heap):
                for item in frontier.heap:
                    if item[2][0] == child[0]:
                        current_cost = problem.getCostOfActions(item[2][1])

                if current_cost > problem.getCostOfActions(path+[child[1]]):
                    frontier.update([child[0], path+[child[1]]], problem.getCostOfActions(path+[child[1]]))



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    node = problem.getStartState()
    path = []
    queue = util.PriorityQueue()
    evalfn = problem.getCostOfActions(path)+heuristic(node, problem)  # f(n)=g(n)+h(n)
    queue.push([node, path], evalfn)
    explored_set = []
    while 1:
        if queue.isEmpty():
            return []  # Failure
        node, path = queue.pop()
        if problem.isGoalState(node):
            return path
        explored_set.append(node)
        succ = problem.getSuccessors(node)
        for child in succ:
            if child[0] not in explored_set and child[0] not in (item[2][0] for item in queue.heap):
                evalfn = problem.getCostOfActions(path+[child[1]])+heuristic(child[0], problem)
                # We push in the stack the successor
                # and the actions which were needed to get to the parent+ the action to successor
                #   and then we use as priority the evaluation function
                queue.push([child[0], path+[child[1]]], evalfn)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
