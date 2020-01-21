"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.stack import Stack
from pacai.util.queue import Queue
from pacai.util.priorityQueue import PriorityQueue

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
    root_successors = problem.successorStates(problem.startingState())
    visited = []
    visited.append(problem.startingState())
    stack = Stack()
    for successor in root_successors:
        stack.push((successor, [successor[1]]))
        visited.append(successor[0])

    while not stack.isEmpty():
        parent = stack.pop()
        successor, path = parent
        if problem.isGoal(successor[0]):
            return path

        for next_successor in problem.successorStates(successor[0]):
            # add unexpanded to nodes to explore
            state, direction, _ = next_successor
            temp_path = path.copy()
            if state not in visited:
                temp_path.append(direction)
                item_to_push = (next_successor, temp_path)
                stack.push(item_to_push)
                visited.append(state)

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    if problem.isGoal(problem.startingState()):
        return []
    queue = Queue()
    queue_list = []
    visited = []
    visited.append(problem.startingState())
    root = ((problem.startingState(), None, 0), [])
    queue.push(root)
    queue_list.append(problem.startingState())
    while not queue.isEmpty():
        parent = queue.pop()
        successor, path = parent
        queue_list.remove(successor[0])
        next_successors = problem.successorStates(successor[0])

        for next_successor in next_successors:
            state, direction, _ = next_successor
            if state not in queue_list and state not in visited:
                temp_path = path.copy()
                temp_path.append(direction)
                if problem.isGoal(state):
                    return temp_path
                item_to_push = (next_successor, temp_path)
                queue.push(item_to_push)
                queue_list.append(next_successor[0])
                visited.append(state)

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***

    pqueue = PriorityQueue()
    pqueue_list = []
    visited = []
    root = ((problem.startingState(), None, 0), [], 0)
    pqueue.push(root, root[2])
    pqueue_list.append(problem.startingState())
    visited.append(problem.startingState())
    while not pqueue.isEmpty():
        parent = pqueue.pop()
        successor, path, path_cost = parent
        pqueue_list.remove(successor[0])

        if problem.isGoal(successor[0]):
            return path

        next_successors = problem.successorStates(successor[0])
        for next_successor in next_successors:
            state, direction, cost = next_successor

            if state not in pqueue_list and state not in visited:
                temp_path = path.copy()
                temp_path.append(direction)
                item_to_push = (next_successor, temp_path, problem.actionsCost(temp_path))
                pqueue.push(item_to_push, problem.actionsCost(temp_path))
                pqueue_list.append(state)
                visited.append(state)

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # heuristic is a function

    # *** Your Code Here ***
    pqueue = PriorityQueue()
    pqueue_list = []
    visited = []
    visited.append(problem.startingState())
    start = (problem.startingState(), None, 0)
    start_heuristic = heuristic(problem.startingState(), problem)
    root = (start, [], 0, start_heuristic)
    pqueue.push(root, root[2] + root[3])
    pqueue_list.append(problem.startingState())
    while not pqueue.isEmpty():
        parent = pqueue.pop()
        successor, path, path_cost, prev_heuristic = parent
        pqueue_list.remove(successor[0])

        if problem.isGoal(successor[0]):
            return path

        next_successors = problem.successorStates(successor[0])
        for next_successor in next_successors:
            state, direction, cost = next_successor
            new_heuristic = heuristic(state, problem)

            if state not in pqueue_list and state not in visited:
                temp_path = path.copy()
                temp_path.append(direction)
                priority = problem.actionsCost(temp_path)
                item_to_push = (next_successor, temp_path, priority, new_heuristic)
                pqueue.push(item_to_push, priority + new_heuristic)
                pqueue_list.append(state)
                visited.append(state)
