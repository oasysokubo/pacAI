"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util import stack
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
    node = problem.startingState()

    # initialize the explored set to be empty
    exploded = set()

    stateDic = {}         # dict to store state (key) and its previos state and action from prevState
    preState = 'none'     # initial as 'none' (dummy value)
    action = 'Stop'       # initial as 'Stop' (dummy value)

    #initialize fringe with initial state
    fringe = stack.Stack()

    return firstSearch(problem, fringe, node, action, preState, stateDic, exploded)

from pacai.util import queue
def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    node = problem.startingState()    # contain position of agent and other (corner, or food information) 

    # initialize the explored set to be empty
    exploded = set()

    stateDic = {}         # dict to store state (key) and its previos state and action from prevState
    preState = 'none'     # initial as 'none' (dummy value)
    action = 'Stop'       # initial as 'Stop' (dummy value)

    #initialize fringe with initial state
    fringe = queue.Queue()
    
    return firstSearch(problem, fringe, node, action, preState, stateDic, exploded)

from pacai.util import priorityQueue
def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    node = problem.startingState()    # contain position of agent and other (corner, or food information)

    # initialize the explored set to be empty
    exploded = set()

    stateDic = {}        # dict to store state (key) and its previos state and action from prevState
    preState = 'none'    # initial as 'none'  (dummy value)
    action = 'Stop'      # initial as 'Stop'  (dummy value)

    #initialize fringe with initial state
    fringe = priorityQueue.PriorityQueue()

    # put initail state, its direction, cost, previosu state and previous heading direction
    fringe.push((node, action, 0 ,preState, action), 0)


    while not fringe.isEmpty():
        node, action, cost, preState, preDir = fringe.pop()   # choose the state with the smallest priority value

        if not ( node ) in exploded:
            exploded.add( (node ) )
            stateDic[(node, action)] = (preState, preDir)     # set node as exploded and bookkeeping
            if (problem.isGoal( node )):
                return PathCreate(problem.startingState(), node, action, stateDic) # get path from bookkeeping structure (stateDic)

            succStates  = problem.successorStates(node)
            for v in succStates:
                if not (v[0]) in exploded:
                    fringe.push( (v[0], v[1], cost + v[2], node, action ), cost + v [2] )  # record next successor, its action... and storage total costs during the path


    return [] # search all path but fail

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    node = problem.startingState()    # contain position of agent and other (corner, or food information)

    # initialize the explored set to be empty
    exploded = set()

    stateDic = {}         # dict to store state (key) and its previos state and action
    preState = 'none'     # initial as 'none' (dummy value)
    action = 'Stop'       # initial as 'Stop' (dummy value)

    #initialize fringe with initial state
    fringe = priorityQueue.PriorityQueue()

    # put initail state, its direction, cost, previosu state and previous heading direction
    fringe.push((node, action, 0, preState, action), 0)


    while not fringe.isEmpty():
        node, action, cost, preState, preDir = fringe.pop()   # choose the state with the smallest priority value

        if not ( node ) in exploded:
            exploded.add( (node ) )
            stateDic[(node, action)] = (preState, preDir)     # set node as exploded and bookkeeping
            if (problem.isGoal( node )):
                #import pdb; pdb.set_trace()
                return PathCreate(problem.startingState(), node, action, stateDic) # get path from bookkeeping structure (stateDic)

            succStates  = problem.successorStates(node)
            for v in succStates:
                if not (v[0]) in exploded:
                    h_n = heuristic( v[0] , problem)
                    fringe.push( (v[0], v[1], cost + v[2], node, action ), h_n + cost + v [2] ) # record next successor, its action... and storage total costs during the path + heristic value


    return [] # search all path but fail


# collecting the path from bookkeeping structure (stateDic)
def PathCreate(start, goal, action, stateDic):
    solution=[]
    solution.append(action)   # put last step (to goal) in list
    preNode, direction = stateDic[(goal,action)]      # use goal ans its action to track previous state and previos action
    solution.insert(0, direction)
    while not (preNode, direction) == (start,'Stop'):       # keep tracking until arrive starting state
        preNode, direction = stateDic[(preNode, direction)]
        solution.insert(0, direction)

    #print solution
    solution.pop(0)     # pop out unnecessary 'Stop' action in intial position
    return solution

# Helper function for searches
def firstSearch(problem, fringe, node, action, preState, stateDic, exploded):
    # put initail state, its direction, cost, previosu state and previous heading direction
    fringe.push((node, action, [], preState, action))     
    
    while not fringe.isEmpty():
        node, action, cost, preState, preDir = fringe.pop()       # choose the last state

        if not ( node ) in exploded:
            exploded.add( (node) )    
            stateDic[(node, action)] = (preState, preDir)         # set node as exploded and bookkeeping
            if (problem.isGoal( (node) )):                        # check if reach gaol state
                return PathCreate(problem.startingState(), node, action, stateDic)    # get path from bookkeeping structure (stateDic)

            succStates  = problem.successorStates(node)           # get successor state
            for v in succStates:
                if not (v[0]) in exploded:
                    fringe.push( (v[0], v[1], v[2], node, action ) )    # record next successor, its action, its cost, and current node & its heading direction

    return [] # search all path but fail