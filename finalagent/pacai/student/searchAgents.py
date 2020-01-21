"""
This file contains incomplete versions of some agents that can be selected to control Pacman.
You will complete their implementations.

Good luck and happy searching!
"""

import logging
import time

from pacai.core.actions import Actions
from pacai.core.directions import Directions
from pacai.core import distance
from pacai.core.search.position import PositionSearchProblem
from pacai.core.search.problem import SearchProblem
from pacai.student import search
from pacai.agents.base import BaseAgent
from pacai.agents.search.base import SearchAgent

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
        self.cornersVisited = []

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
        return (self.startingPosition, self.cornersVisited)

    def isGoal(self, state):
        pos, visitedCorners = state
        self._visitedLocations.add(pos)
        self._visitHistory.append(pos)
        if pos not in self.corners:
            return False
        return len(visitedCorners) == len(self.corners)

    def successorStates(self, state):
        successors = []

        for action in Directions.CARDINAL:
            pos, visitedCorners = state
            x, y = pos
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]

            if (not hitsWall):
                # Construct the successor.
                nextPos = (nextx, nexty)
                if nextPos in self.corners:
                    temp_visitedCorners = visitedCorners.copy()
                    if nextPos not in visitedCorners:
                        temp_visitedCorners.append(nextPos)
                        cost = 1
                        nextState = (nextPos, temp_visitedCorners)
                        successors.append((nextState, action, cost))
                        continue
                cost = 1
                nextState = (nextPos, visitedCorners)
                successors.append((nextState, action, cost))
        self._numExpanded += 1
        if (state[0] not in self._visitedLocations):
            self._visitedLocations.add(state[0])
            self._visitHistory.append(state[0])

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
    coord, visitedCorners = state
    corners = problem.corners
    h = [(c, distance.manhattan(coord, c)) for c in corners if c not in visitedCorners]
    h.sort(reverse=True, key=lambda h: h[1])
    if len(h) == 0:
        return 0
    # closest = h[-1]
    # # print(closest)
    # max_h = distance.manhattan(coord, closest[0])
    # for i in range(len(h)-1):
    #     # if (i+1) > len(h):
    #     #     break
    #     furthest, _ = h[i]
    #     next_furthest, _ = h[i+1]
    #     max_h += distance.manhattan(next_furthest, furthest)
    # return max_h
    if len(h) == 0:
        return 0
    elif len(h) < 2:
        furthest = h[0]
        return furthest[1]
    furthest = h[0]
    second_furthest = h[-1]     # closest
    tmp_h1 = distance.manhattan(coord, second_furthest[0])
    tmp_h2 = distance.manhattan(second_furthest[0], furthest[0])
    # print('Heuristic to furthest: ', furthest[1])
    # print('Heuristic to second furthest plus furthest: ', tmp_h1 + tmp_h2)
    return tmp_h1 + tmp_h2

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
    coord, foodGrid = state
    food_list = foodGrid.asList()
    h = [(food, distance.manhattan(coord, food)) for food in food_list]
    h.sort(reverse=True, key=lambda h: h[1])
    if len(h) == 0:
        return 0
    elif len(h) < 2:
        furthest = h[0]
        return furthest[1]
    # elif len(h) < 3:
    furthest = h[0]
    closest = h[-1]
    # second_closest = h[-2]
    tmp_h1 = distance.manhattan(coord, closest[0])
    tmp_h2 = distance.manhattan(closest[0], furthest[0])
    return tmp_h1 + tmp_h2

    # furthest = h[0]
    # closest = h[-1]
    # second_closest = h[1]
    # tmp_h1 = distance.manhattan(coord, closest[0])
    # tmp_h2 = distance.manhattan(closest[0], second_closest[0])
    # tmp_h3 = distance.manhattan(second_closest[0], furthest[0])
    # return tmp_h2 + tmp_h1 + tmp_h3

    # furthest = h[0]
    # second_furthest = h[1]
    # third_furthest = h[2]
    # tmp_h1 = distance.manhattan(coord, third_furthest[0])
    # tmp_h2 = distance.manhattan(third_furthest[0], second_furthest[0])
    # tmp_h3 = distance.manhattan(second_furthest[0], furthest[0])
    # return tmp_h1 + tmp_h2 + tmp_h3

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
        return search.breadthFirstSearch(problem)

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

    def isGoal(self, state):
        return state in self.food.asList()

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

    # The basic idea for this agent is to return a path
    # as quick as possible. This is done by creating a
    # new problem called ApproxProblem that extends the
    # CornerProblem. By doing so, we are now interested
    # in eating all the food in the gameState instead of
    # reaching all the corners.

    # I chose to use DFS as the search algorithm because
    # level-first search algorithms spend too much
    # computation time trying to find the optimal path.
    # This is too expensive for our case, thus we chose
    # DFS for a significantly less expensive computational
    # requirement inexchange for a non-optimal solution.

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def registerInitialState(self, state):
        starttime = time.time()

        currentState = state
        problem = ApproxProblem(currentState)
        self._actions = search.depthFirstSearch(problem)
        self._actionIndex = 0

        totalCost = problem.actionsCost(self._actions)

        state.setHighlightLocations(problem.getVisitHistory())

        logging.info('Path found with total cost of %d in %.1f seconds' %
                (totalCost, time.time() - starttime))

        logging.info('Search nodes expanded: %d' % problem.getExpandedCount())

    def getAction(self, state):
        if (self._actionIndex >= (len(self._actions))):
            return Directions.STOP

        action = self._actions[self._actionIndex]
        self._actionIndex += 1

        return action

class ApproxProblem(SearchProblem):

    def __init__(self, startingGameState):
        super().__init__()

        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()

        food_list = startingGameState.getFood().asList()
        self.food = ()
        for food in food_list:
            self.food = (*self.food, food)

        # *** Your Code Here ***
        self.foodEaten = []

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
        return (self.startingPosition, self.foodEaten)

    def isGoal(self, state):
        pos, visitedCorners = state
        self._visitedLocations.add(pos)
        self._visitHistory.append(pos)
        if pos not in self.food:
            return False
        return len(visitedCorners) == len(self.food)

    def successorStates(self, state):
        successors = []

        for action in Directions.CARDINAL:
            pos, visitedCorners = state
            x, y = pos
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]

            if (not hitsWall):
                # Construct the successor.
                nextPos = (nextx, nexty)
                if nextPos in self.food:
                    temp_visitedCorners = visitedCorners.copy()
                    if nextPos not in visitedCorners:
                        temp_visitedCorners.append(nextPos)
                        cost = 1
                        nextState = (nextPos, temp_visitedCorners)
                        successors.append((nextState, action, cost))
                        continue
                cost = 1
                nextState = (nextPos, visitedCorners)
                successors.append((nextState, action, cost))
        self._numExpanded += 1
        if (state[0] not in self._visitedLocations):
            self._visitedLocations.add(state[0])
            self._visitHistory.append(state[0])

        return successors
