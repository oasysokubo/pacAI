"""
In this file, you will implement generic search algorithms which are called by Pacman agents.

Author: Oasys Okubo
Class:  CSE 140 - Artificial Intelligence
Date:   October 17, 2019
"""

from pacai.util import queue
from pacai.util import stack
from pacai.util import priorityQueue

def fringeState(problem, node, action, undefinedState, status = 'none'):
    """
    initialize fringe with initial state
    put initail state, its direction, cost, previosu state and previous heading direction
    """
    if status == 'uniform':  # Use a priority queue for uniformsearch
        fringe = priorityQueue.PriorityQueue()
        fringe.push((node, action, 0, undefinedState, action), 0)
    elif status == 'aStar':  # Use a priority queue for astarsearch
        fringe = priorityQueue.PriorityQueue()
        fringe.push((node, action, 0, undefinedState, action), 0)
    elif status == 'breadth':  # Use a queue for breadthfirstsearch
        fringe = queue.Queue()
        fringe.push((node, action, [], undefinedState, action))
    elif status == 'depth':  # Use a stack for depthfirstsearch
        fringe = stack.Stack()
        fringe.push((node, action, [], undefinedState, action))
    else:
        pass
    return fringe

# Helper function for all search algorithms
def firstSearch(problem, heuristic = None, status = 'none'):
    """
    status:
        Breadth/Depth:  status = 'none'
        Uniform:        status = 'uniform'
        aStar:          status = 'aStar'
    """
    node = problem.startingState()  # Get the starting state from respective problem
    currentState = {}  # Track each state of direction in the maze
    fringe = fringeState(problem = problem, node = node, action = 0, undefinedState = -1,
    status = status)  # Function call to initialize data structure to hold action values
    visited = set()
    while len(fringe) > 0:  # While fringe is not empty
        node, action, cost, undefinedState, undefinedMove = fringe.pop()

        if (node) not in visited:  # Check to see if starting state is not yet visited
            visited.add((node))  # Add node to the visited list to keep track of already visited
            # Update the current state to keep track in a dict
            currentState[(node, action)] = (undefinedState, undefinedMove)
            if (problem.isGoal((node))):  # Check if all four corners are visited in the maze
                final_path = []
                final_path.append(action)
                prevMove, direction = currentState[(node, action)]
                final_path.insert(0, direction)

                # While these tuples don't equal eachother to not create double instances
                while (prevMove, direction) != (problem.startingState(), 0):
                    prevMove, direction = currentState[(prevMove, direction)]
                    final_path.insert(0, direction)
                    print(direction)

                final_path.pop(0)  # Remove the first redundant value of the list
                return final_path  # Return the final optimal path to take to a destination

            # Get all current successors from the current node
            successorState = problem.successorStates(node)
            # Iterate through all existing successors from a specific node
            for successor in successorState:
                if (successor[0]) not in visited:  # If the successor is not yet visited
                    if status == 'uniform':  # Update priority queue with cost, node, and action
                        fringe.push((successor[0], successor[1], cost + successor[2], node, action),
                        cost + successor[2])
                    elif status == 'aStar':  # Update priority queue with cost, node, and action
                        heuristicVal = heuristic(successor[0], problem)
                        fringe.push((successor[0], successor[1], cost + successor[2], node, action),
                        heuristicVal + cost + successor[2])
                    else:  # Update stack/queue with node and action
                        fringe.push((successor[0], successor[1], successor[2], node, action))
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
