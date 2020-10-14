from pacai.agents.capture.reflex import ReflexCaptureAgent
from pacai.util import reflection, counter
from pacai.core.directions import Directions


def createTeam(firstIndex, secondIndex, isRed,
        first = '',
        second = ''):
    """
    This function should return a list of two agents that will form the capture team,
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


class DefensiveReflexAgent(ReflexCaptureAgent):
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

        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0).
        features['onDefense'] = 1
        if (myState.isPacman()):
            features['onDefense'] = 0

        # Computes distance to invaders we can see.
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman() and a.getPosition() is not None]
        features['numInvaders'] = len(invaders)

        if (len(invaders) > 0):
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)

        if (action == Directions.STOP):
            features['stop'] = 1

        rev = Directions.REVERSE[gameState.getAgentState(self.index).getDirection()]
        if (action == rev):
            features['reverse'] = 1

        return features

    def getWeights(self, gameState, action):
        return {
            'numInvaders': -1000,
            'onDefense': 200,
            'invaderDistance': -20,
            'stop': -100,
            'reverse': -2
        }

class OffensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that seeks food.
    This agent will give you an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = counter.Counter()
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.getScore(successor)

        # Compute distance to the nearest food.
        foodList = self.getFood(successor).asList()
        GhostIList = self.getOpponents(gameState)
        GhostList = [successor.getAgentState(i).getPosition() for i in GhostIList]

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance
        if (len(GhostList) > 0):
            dist = []
            myPos = successor.getAgentState(self.index).getPosition()
            for i in GhostIList:
                if successor.getAgentState(i).getScaredTimer() <= 1:
                    dist.append(self.getMazeDistance(myPos, successor.getAgentState(i).getPosition()))
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
            'distanceToGhost': -2
        }

#class CustomAgent(CaptureAgent):
#    def __init__(self, index, **kwargs):
#        super().__init__(index, **kwargs)
#        self.gridPoints = []
#        self.features = {'default' : 1} # future futures could include position of the gridpoint
#
#    def chooseAction(self, gameState):
#        self.generateGridPoints(gameState)
#        mapping = self.generateMapping()
#        return 'Stop' # default action is returned
#
#    def generateGridPoints(self, gameState):
#        walls = gameState.getWalls().asList()
#        maxx = 0
#        maxy = 0
#        for wall in walls:
#            x, y = wall
#            maxx = max(maxx, x)
#            maxy = max(maxy, y)
#        points = [(x, y) for x in range(maxx)
#                            for y in range(maxy)
#                                if not gameState.hasWall(x, y)]
#        self.gridPoints = points
#
#    def reward(self, *args):
#        # args is a list of args, of which could contain gridpoints, ...,
#        # and other info used to calculate the reward
#        # features is a map of features to real values
#        weights = counter.Counter() # weights are currently the identity
#        n = 0
#        for feature in self.features:
#            weights[feature] = 1
#            n += (weights[feature] * self.features[feature])
#        return n
#
#    def generateMapping(self):
#        mapping = []
#        for gridpoint in self.gridPoints:
#            item = (gridpoint, self.reward())
#            mapping.append(item)
#        return mapping
