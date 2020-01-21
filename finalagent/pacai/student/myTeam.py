from pacai.agents.capture.capture import CaptureAgent
from pacai.util import counter
from pacai.agents.capture.reflex import ReflexCaptureAgent
from pacai.core.directions import Directions
import random


def createTeam(firstIndex, secondIndex, isRed, first='', second=''):
    """
    This function should return a
     list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    firstAgent = OffensiveReflexAgent
    secondAgent = DefensiveReflexAgent

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]


class CustomAgent(CaptureAgent):
    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
        self.gridPoints = None
        self.deadends = []
        self.visited = set()
        self.chokepoints = []
        self.mapping = None
        self.mySide = []
        self.enemySide = []
        self.maxx = None
        self.maxy = None
        self.chokepointMapping = {}
        self.food = None

    def registerInitialState(self, gameState):
        super().registerInitialState(gameState)

        def findDeadEnd(gridpoints):
            def countActions(point):
                x, y = point
                action_list = []
                up = (x, y + 1)
                down = (x, y - 1)
                left = (x - 1, y)
                right = (x + 1, y)
                if left in self.gridPoints:
                    action_list.append(left)
                if right in self.gridPoints:
                    action_list.append(right)
                if down in self.gridPoints:
                    action_list.append(down)
                if up in self.gridPoints:
                    action_list.append(up)
                return len(action_list), action_list

            for p in gridpoints:
                num_actions, action_list = countActions(p)
                if num_actions == 0:
                    raise ValueError("Illegal Action")
                if num_actions == 1:
                    # add initial position that is classified as a deadend
                    item = (p)
                    if item not in self.deadends:
                        self.deadends.append(item)

        self.generateGridPoints(gameState)
        findDeadEnd(self.gridPoints)
        self.updateChokePoints(self.deadends, gameState)
        self.food = gameState.getFood().asList()

        # print('chokepoints', self.chokepoints)
        # print('enemy chokepoints', self.enemySide)
        # print('my chokepoints', self.mySide)

    def chooseAction(self, gameState):
        return 'Stop'

    def resetVariables(self):
        self.visited.clear()
        self.chokepoints = []
        self.enemySide = []
        self.mySide = []
        self.chokepointMapping = {}

    def updateChokePoints(self, deadends, gameState):
        self.resetVariables()
        self.findChokePoint(self.deadends, gameState)
        tmp = []
        for elem in self.chokepoints:
            position, steps, food = elem
            if food == 0:
                continue
            x, y = position
            item = (position, 2 * steps, food)
            tmp.append(item)
            self.chokepointMapping[position] = (2 * steps, food)
            if (x >= 0 and x < (self.maxx / 2)
                    and not gameState.isOnRedTeam(self.index)):
                self.enemySide.append(item)
            else:
                self.mySide.append(item)
        self.chokepoints = tmp

        # highlight grid
        for elem in self.chokepoints:
            self.visited.add(elem[0])
        gameState.setHighlightLocations(self.visited)

    def findChokePoint(self, deadends, gameState):
        # setup a list, initially no visited grid
        visitedList = []

        def possibleActions(position):
            x, y = position
            actions = []
            up = (x, y + 1)
            down = (x, y - 1)
            left = (x - 1, y)
            right = (x + 1, y)
            if left in self.gridPoints and left not in visitedList:
                actions.append(left)
            if right in self.gridPoints and right not in visitedList:
                actions.append(right)
            if down in self.gridPoints and down not in visitedList:
                actions.append(down)
            if up in self.gridPoints and up not in visitedList:
                actions.append(up)
            return actions

        def dfs(curr, prev, knownGrids, visited, num_food):
            if prev is None:
                L = possibleActions(curr)
                if len(L) != 1:
                    if gameState.hasFood(*curr):
                        item = (curr, len(visited), num_food + 1)
                        self.chokepoints.append(item)
                    else:
                        self.chokepoints.append((curr, len(visited), num_food))
                    return
                else:
                    # check if there exist a temp choke point
                    cpi = 0
                    for c in self.chokepoints:
                        if c[0] == curr:
                            del self.chokepoints[cpi]
                        cpi += 1

                    # append the visited grid to a list
                    visitedList.append(curr)

                    visited.append(curr)
                    if gameState.hasFood(*curr):
                        dfs(L[0], curr, knownGrids, visited, num_food + 1)
                    else:
                        dfs(L[0], curr, knownGrids, visited, num_food)
            else:
                L = possibleActions(curr)
                if len(L) == 0:
                    pass
                if len(L) != 1:
                    if gameState.hasFood(*curr):
                        item = (curr, len(visited), num_food + 1)
                        self.chokepoints.append(item)
                    else:
                        self.chokepoints.append((curr, len(visited), num_food))
                    return
                else:
                    # check if there exist a temp choke point
                    cpi = 0
                    for c in self.chokepoints:
                        if c[0] == curr:
                            del self.chokepoints[cpi]
                        cpi += 1

                    # append the visited grid to a list
                    visitedList.append(curr)

                    visited.append(curr)
                    if gameState.hasFood(*curr):
                        dfs(L[0], curr, knownGrids, visited, num_food + 1)
                    else:
                        dfs(L[0], curr, knownGrids, visited, num_food)
        for d in deadends:
            if gameState.hasFood(*d):
                dfs(d, None, self.gridPoints, [], 1)
            else:
                dfs(d, None, self.gridPoints, [], 0)

    def generateGridPoints(self, gameState):
        walls = gameState.getWalls().asList()
        maxx = 0
        maxy = 0
        for wall in walls:
            x, y = wall
            maxx = max(maxx, x)
            maxy = max(maxy, y)
        points = [
            (x, y)
            for x in range(maxx) for y in range(maxy)
            if not gameState.hasWall(x, y)]
        self.maxx = maxx
        self.maxy = maxy
        self.gridPoints = points

    def getPositionFromAction(self, position, action):
        x, y = position
        if action == 'North':
            return (x, y + 1)
        elif action == 'South':
            return (x, y - 1)
        elif action == 'West':
            return (x - 1, y)
        elif action == 'East':
            return (x + 1, y)
        elif action == 'Stop':
            return position

    def findItemInList(self, item, List):
        for elem in List:
            p, b, n = elem
            if p == item:
                return True
        return False

    def distGhostToPacman(self, gameState):
        my_pos = gameState.getAgentPosition(self.index)
        ghost_pos = [
            gameState.getAgentState(i).getPosition()
            for i in self.getOpponents(gameState)]
        dist_between = [self.getMazeDistance(my_pos, gp) for gp in ghost_pos]
        sorted(dist_between)
        return dist_between[0]


class OffensiveReflexAgent(ReflexCaptureAgent, CustomAgent):
    """
    A reflex agent that seeks food.
    This agent will give you an idea of what
     an offensive agent might look like,
    but it is by no means the best or only
     way to build an offensive agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def chooseAction(self, gameState):
        """
        Picks among the actions with the
        highest return from `ReflexCaptureAgent.evaluate`.
        """
        if self.food != gameState.getFood().asList():
            self.food = gameState.getFood().asList()
            self.updateChokePoints(self.deadends, gameState)
            # print('enemy chokepoints', self.enemySide)
        actions = gameState.getLegalActions(self.index)

        values = [self.evaluate(gameState, a) for a in actions]

        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]

        if 'Stop' in bestActions and len(bestActions) != 1:
            bestActions.remove('Stop')

        return random.choice(bestActions)

    def getFeatures(self, gameState, action):
        features = counter.Counter()
        chokepoints = self.enemySide
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()
        pos_from_action = self.getPositionFromAction(myPos, action)
        if self.findItemInList(pos_from_action, chokepoints):
            s = self.chokepointMapping[pos_from_action][0]
            f = self.chokepointMapping[pos_from_action][1]
            # trying out random factors
            features['chokepoint'] = (-s + f)
        else:
            features['chokepoint'] = -3
        features['successorScore'] = self.getScore(successor)

        # Compute distance to the nearest food.
        foodList = self.getFood(successor).asList()

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([
                self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance

        GhostIList = self.getOpponents(gameState)
        GhostList = [
            successor.getAgentState(i).getPosition() for i in GhostIList]
        if (len(GhostList) > 0):
            dist = []
            myPos = successor.getAgentState(self.index).getPosition()
            for i in GhostIList:
                if successor.getAgentState(i).getScaredTimer() <= 1:
                    dist.append(self.getMazeDistance(
                        myPos, successor.getAgentState(i).getPosition()))
            if len(dist) > 0:
                minDistance = min(dist)
                features['distanceToGhost'] = 1 / minDistance
            else:
                features['distanceToGhost'] = 0

        return features

    def getWeights(self, gameState, action):
        return {
            'successorScore': 100,
            'distanceToFood': -1,
            'chokepoint': 0.2,
            'distanceToGhost': -2
        }


class DefensiveReflexAgent(ReflexCaptureAgent, CustomAgent):
    """
    A reflex agent that tries to keep its side Pacman-free.
    This is to give you an idea of what a defensive agent could be like.
    It is not the best or only way to make such an agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = counter.Counter()
        successor = self.getSuccessor(gameState, action)
        
        
        self.index2 = (self.index + 2) % 4
        if self.red: side = -2
        else: side =2
        
        
        walls = gameState.getWalls()

        gameBoardHeight= walls.getHeight()
        gameBoardWidth = walls.getWidth()

        centerLine = gameBoardWidth/2


        #find the opening closest to the middle
        middleOpening = (centerLine, 0)


        for i in range(1, gameBoardHeight-1):
          if not walls[int(centerLine)][i] and not walls[int(centerLine + side)][i]:
            defensiveOpenings.append((centerLine + side, i))

        dist = []
        for (doX, doY) in defensiveOpenings:
          d = abs(gameBoardHeight/2 - doY)
          dist.append((d, (doX, doY)))

        middleOpening = min(dist)[1]
        
        print('Middle: ', middleOpening)
        
        
        midx = int(self.maxx / 2) + 1
        midy = int(self.maxy / 2) + 1
        if gameState.hasWall(midx, midy):
            for elem in self.gridPoints:
                x, y = elem
                if abs(x - midx) <= 1:
                    midx = x
                    midy = y
                    break


        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        distToMid = self.getMazeDistance(myPos, (midx, midy))

        features['defendMid'] = -distToMid

        # Computes whether we're on defense (1) or offense (0).
        features['onDefense'] = 1
        if (myState.isPacman()):
            features['onDefense'] = 0

        # Computes distance to invaders we can see.
        enemies = [
            successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [
            a for a in enemies if a.isPacman() and a.getPosition() is not None]
        features['numInvaders'] = len(invaders)

        if len(invaders) > 0:
            features['defendMid'] = 1

        if (len(invaders) > 0):
            dists = [
                self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)

        if (action == Directions.STOP):
            features['stop'] = 1

        rev = Directions.REVERSE[
            gameState.getAgentState(self.index).getDirection()]
        if (action == rev):
            features['reverse'] = 1

        return features

    def getWeights(self, gameState, action):
        return {
            'numInvaders': -1000,
            'onDefense': 100,
            'invaderDistance': -10,
            'stop': -100,
            'reverse': -0.5,
<<<<<<< HEAD:finalagent/pacai/student/myTeam.py
            'defendMid': 10,
            'defendMidTop': 0,
            'defendMidBot': 0
=======
            'defendMid': 10
>>>>>>> 9f05377a18c5a4442314640fc64bce92ce565a8c:pacai/student/myTeam.py
        }
