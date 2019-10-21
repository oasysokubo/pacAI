"""
This file contains incomplete versions of some agents that can be selected to control Pacman.
You will complete their implementations.

Good luck and happy searching!


Author: Oasys Okubo
Class:  CSE 140 - Artificial Intelligence
Date:   October 17, 2019
"""

import logging

from pacai.core.actions import Actions
from pacai.core.search import heuristic
from pacai.core.search.position import PositionSearchProblem
from pacai.core.search.problem import SearchProblem
from pacai.agents.base import BaseAgent
from pacai.agents.search.base import SearchAgent
from pacai.core.directions import Directions
from pacai.core import distance
from pacai.student import search

class CornersProblem(SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function.
    See the `pacai.core.search.position.PositionSearchProblem` class for an example of
    a working SearchProblem.

    Additional methods to implement:

    `pacai.core.search.problem.SearchProblem.startingState`:
    Returns the start state (in your search space,
    NOT a `pacai.core.gamestate.AbstractGameState`).

    `pacai.core.search.problem.SearchProblem.isGoal`:
    Returns whether this search state is a goal state of the problem.

    `pacai.core.search.problem.SearchProblem.successorStates`:
    Returns successor states, the actions they require, and a cost of 1.
    The following code snippet may prove useful:
    ```
        successors = []

        for action in Directions.CARDINAL:
            x, y = currentPosition
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]

            if (not hitsWall):
                # Construct the successor.

        return successors
    ```
    """

    def __init__(self, startingGameState):
        super().__init__()

        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top = self.walls.getHeight() - 2
        right = self.walls.getWidth() - 2

        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                logging.warning('Warning: no food in corner ' + str(corner))

        # *** Your Code Here ***
        # self.cost = lambda x:1      # Successors actions cost 1
        self._numExpanded = 0       # Count how many nodes expanded

    def actionsCost(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        If those actions include an illegal move, return 999999.
        This is implemented for you.
        """

        if (actions is None):
            return 999999

        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999

        return len(actions)

    def startingState(self):
        """
        Returns the start state (in your search space,
        NOT a `pacai.core.gamestate.AbstractGameState`).
        """
        return (self.startingPosition, (False, False, False, False))        # Returns starting position and 4 false because no corners are visited yet

    def isGoal(self, state):
        """
        Returns whether this search state is a goal state of the problem.
        """

        currentState = state[1]
        return currentState[0] and currentState[1] and currentState[2] and currentState[3]

    def successorStates(self, state):
        """
        Updates visited corners to its respective boolean value
        Returns successor states, the actions they require, and a cost of 1.
        """
        currentState = state[1]
        successors = []
        for action in Directions.CARDINAL:
            x, y = state[0]     # currentPosition
            print("State: {}".format(state[0]))
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]

            if (not hitsWall):  # Implement a successor discovery
                successors.append((
                ((nextx,nexty),(
                ((nextx, nexty) == self.corners[0]) or state[1][0],
                ((nextx, nexty) == self.corners[1]) or state[1][1],
                ((nextx, nexty) == self.corners[2]) or state[1][2],
                ((nextx, nexty) == self.corners[3]) or state[1][3])
                ), action, 1))
            
                # nextxy = (nextx, nexty) 
                # successorPost = None
                # if nextxy in self.corners:
                #     # successor = [successorState[0], successorState[1], successorState[2], successorState[3]]
                #     for corner in range(len(self.corners)):
                #         print("nextxy {}\ncorner {}".format(nextxy, self.corners[corner]))
                #         if nextxy == self.corners[corner]:
                #             # successor[corner] = currentState[corner]
                #             successors = True
                #         else:
                #             successor[corner] = currentState[corner]
                #     print(len(successors))
                #     successorPost = (successors[0], successors[1], successors[2], successors[3])
                # successors.append(((nextxy, successorPost), action, 1))

        self._numExpanded += 1
        return successors

def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

    This function should always return a number that is a lower bound
    on the shortest path from the state to a goal of the problem;
    i.e. it should be admissible.
    (You need not worry about consistency for this heuristic to receive full credit.)
    """

    # Useful information.
    # corners = problem.corners  # These are the corner coordinates
    # walls = problem.walls  # These are the walls of the maze, as a Grid.

    # *** Your Code Here ***
    corners = problem.corners  # These are the corner coordinates
    walls = problem.walls  # These are the walls of the maze, as a Grid.

    # Get unvisited corners
    successor = [False, False, False, False]
    currentPosition = state[0]
    currentStatus = state[1]

    for corner in range(len(corners)):
        successor[corner] = distance.manhattan(currentPosition, corners[corner]) * (not currentStatus[corner])
    successor.sort()
    return successor[-1]

def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.
    First, try to come up with an admissible heuristic;
    almost all admissible heuristics will be consistent as well.

    If using A* ever finds a solution that is worse than what uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!
    On the other hand, inadmissible or inconsistent heuristics may find optimal solutions,
    so be careful.

    The state is a tuple (pacmanPosition, foodGrid) where foodGrid is a
    `pacai.core.grid.Grid` of either True or False.
    You can call `foodGrid.asList()` to get a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the problem.
    For example, `problem.walls` gives you a Grid of where the walls are.

    If you want to *store* information to be reused in other calls to the heuristic,
    there is a dictionary called problem.heuristicInfo that you can use.
    For example, if you only want to count the walls once and store that value, try:
    ```
    problem.heuristicInfo['wallCount'] = problem.walls.count()
    ```
    Subsequent calls to this heuristic can access problem.heuristicInfo['wallCount'].
    """

    position, foodGrid = state

    # *** Your Code Here ***
    if len(foodGrid.asList()) is 0: 
        return 0

    maxHeuristic = 0
    trackHeuristic = []
    for food in foodGrid.asList():
        currentHeuristic = distance.manhattan(position, food)
        trackHeuristic.append(currentHeuristic)
    maxHeuristic = max(trackHeuristic)
    return sum(trackHeuristic)/len(trackHeuristic) + len(trackHeuristic) #maxHeuristic 

class ClosestDotSearchAgent(SearchAgent):
    """
    Search for all food using a sequence of searches.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def registerInitialState(self, state):
        self._actions = []
        self._actionIndex = 0

        currentState = state

        while (currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState)  # The missing piece
            self._actions += nextPathSegment

            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' %
                            (str(action), str(currentState)))

                currentState = currentState.generateSuccessor(0, action)

        logging.info('Path found with cost %d.' % len(self._actions))

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from gameState.
        """

        # Here are some useful elements of the startState
        # startPosition = gameState.getPacmanPosition()
        # food = gameState.getFood()
        # walls = gameState.getWalls()
        # problem = AnyFoodSearchProblem(gameState)

        # *** Your Code Here ***
        problem = AnyFoodSearchProblem(gameState)
        return search.uniformCostSearch(problem)

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem,
    but has a different goal test, which you need to fill in below.
    The state space and successor function do not need to be changed.

    The class definition above, `AnyFoodSearchProblem(PositionSearchProblem)`,
    inherits the methods of `pacai.core.search.position.PositionSearchProblem`.

    You can use this search problem to help you fill in
    the `ClosestDotSearchAgent.findPathToClosestDot` method.

    Additional methods to implement:

    `pacai.core.search.position.PositionSearchProblem.isGoal`:
    The state is Pacman's position.
    Fill this in with a goal test that will complete the problem definition.
    """

    def __init__(self, gameState, start = None):
        super().__init__(gameState, goal = None, start = start)

        # Store the food for later reference.
        self.food = gameState.getFood()
        self.startPosition = gameState.getPacmanPosition()
        self.walls = gameState.getWalls()
        # self.cost = lambda x:1
    
    def isGoal(self, state):
        """
        The state is Pacman's position.
        """
        x, y = state
        return (x, y) in self.food.asList()

class ApproximateSearchAgent(BaseAgent):
    """
    Implement your contest entry here.

    Additional methods to implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Get a `pacai.bin.pacman.PacmanGameState`
    and return a `pacai.core.directions.Directions`.

    `pacai.agents.base.BaseAgent.registerInitialState`:
    This method is called before any moves are made.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)
