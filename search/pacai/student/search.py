"""
In this file, you will implement generic search algorithms which are called by Pacman agents.

Author: Oasys Okubo
Class:  CSE 140 - Artificial Intelligence
Date:   October 17, 2019
"""

from pacai.util import queue
from pacai.util import stack
from pacai.util import priorityQueue

def fringeState(problem, node, action, preState, status = 'None'):
    """
    initialize fringe with initial state
    put initail state, its direction, cost, previosu state and previous heading direction
    """
    if status is 'uniform':
        fringe = priorityQueue.PriorityQueue()
        fringe.push((node, action, 0, preState, action), 0)
    elif status is 'aStar':
        fringe = priorityQueue.PriorityQueue()
        fringe.push((node, action, 0, preState, action), 0)
    elif status is 'breadth':
        fringe = queue.Queue()
        fringe.push((node, action, [], preState, action))
    elif status is 'depth':
        fringe = stack.Stack()
        fringe.push((node, action,[], preState, action))

    return fringe

# Helper function for all search algorithms
def firstSearch(problem, heuristic = None, status = 'None'):

    """
    status:
        Breadth/Depth:  status = 'none'
        Uniform:        status = 'uniform'
        aStar:          status = 'aStar'
    """    
    node = problem.startingState()    # contain position of agent and other (corner, or food information)

    # initialize the explored set to be empty
    exploded = set()

    stateDic = {}         # dict to store state (key) and its previos state and action
    preState = 'none'     # initial as 'none' (dummy value)
    action = 'Stop'       # initial as 'Stop' (dummy value)

    fringe = fringeState(problem = problem, node = node, action = action, preState = preState, status = status)

    while not fringe.isEmpty():
        node, action, cost, preState, preDir = fringe.pop()                                     # choose the last state

        if not (node) in exploded:
            exploded.add((node))    
            stateDic[(node, action)] = (preState, preDir)                                       # set node as exploded and bookkeeping
            if (problem.isGoal((node))):                                                        # check if reach gaol state
                #return PathCreate(problem.startingState(), node, action, stateDic)              # get path from bookkeeping structure (stateDic)
                solution=[]
                solution.append(action)                                     # put last step (to goal) in list
                preNode, direction = stateDic[(node, action)]                # use goal ans its action to track previous state and previos action
                solution.insert(0, direction)
                while not (preNode, direction) == (problem.startingState(),'Stop'):           # keep tracking until arrive starting state
                    preNode, direction = stateDic[(preNode, direction)]
                    solution.insert(0, direction)
                    print(direction)

                solution.pop(0)                                             # pop out unnecessary 'Stop' action in intial position
                return solution

            succStates  = problem.successorStates(node)                                         # get successor state
            for v in succStates:
                if not (v[0]) in exploded:
                    if status is 'uniform':
                        fringe.push((v[0], v[1], cost + v[2], node, action), cost + v [2])
                    elif status is 'aStar':
                        h_n = heuristic(v[0] , problem)
                        fringe.push((v[0], v[1], cost + v[2], node, action), h_n + cost + v [2])
                    else:
                        fringe.push((v[0], v[1], v[2], node, action))                           # record next successor, its action, its cost, and current node & its heading direction

    return [] 


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """
    # *** Your Code Here ***
    return firstSearch(problem = problem, status = 'depth')

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """
    # *** Your Code Here ***
    return firstSearch(problem = problem, status = 'breadth')

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    # *** Your Code Here ***
    return firstSearch(problem = problem, status = 'uniform')

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # *** Your Code Here ***
    return firstSearch(problem = problem, heuristic = heuristic, status = 'aStar')