import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent

from pacai.core import distance

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        # newPosition = successorGameState.getPacmanPosition()
        # oldFood = currentGameState.getFood()
        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***
        # if action == 0:
        #     return 0

        newScore = successorGameState.getScore()
        newPosition = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()

        # Heuristics for ghosts
        # Get all ghost positions
        ghostDistances = [ghostState.getPosition() for ghostState in newGhostStates]
        # Get the manhattan distance of curr position and ghosts
        ghostHeuristics = [distance.manhattan(newPosition, ghostDistance)
        for ghostDistance in ghostDistances]

        ghostScore = 0
        for ghostDistance in ghostDistances:  # Iterate through all ghost distances
            # If pacman is not in danger
            if newGhostStates[ghostDistances.index(ghostDistance)].getScaredTimer == 0:
                ghostScore -= 50
            else:  # Otherwise, give reward to get more pellets
                ghostScore = 50

        # Heuristics for foods
        # oldCapsule = currentGameState.getCapsules()
        # print(oldCapsule)

        ghostable = []
        for newState in newGhostStates:  # Iterate through all ghost states
            ghostPosition = newState.getPosition()

            # print("ghost position: ", ghostPosition)
            # print("new scared times: ", newScaredTimes)

            # Append all coordinates of ghost with outskirt radius of 1
            # in order to find danger zone for pacman
            ghostable.append((ghostPosition[0], ghostPosition[1]))
            ghostable.append((ghostPosition[0], ghostPosition[1] - 1))
            ghostable.append((ghostPosition[0], ghostPosition[1] + 1))
            ghostable.append((ghostPosition[0] - 1, ghostPosition[1]))
            ghostable.append((ghostPosition[0] + 1, ghostPosition[1]))
        if len(newFood.asList()) > 0:  # If there is still food left, penalize
            newScore -= distance.manhattan(newPosition, newFood.asList()[0])
        if newPosition in ghostable:  # If pacman is in danger proximity of ghost
            newScore -= 750  # Penalize significantly if inside danger proximity

        newScore += sum(ghostHeuristics) + ghostScore  # final evaluation score
        return newScore


class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getNumAgents(self, gameState):
        """
        Get the total number of agents in the game
        """
        return gameState.getNumAgents()

    def getLegalActions(self, gameState, index):
        """
        Returns a list of legal actions for an agent.
        Pacman is always at index 0, and ghosts are >= 1.
        """
        return gameState.getLegalActions(index)

    def generateSuccessor(self, gameState, legalActions):
        """
        Get the successor game state after an agent takes an action.
        """
        successors = []
        for actions in legalActions:
            action = gameState.generatePacmanSuccessor(actions)
            successors.append(action)
        return successors

    def getTreeDepth(self):
        return self._treeDepth

    def getEvaluationFunction(self, gameState):
        return self._evaluationFunction(gameState)

    def minimax(self, gameState, index, depth):
        """
        Minimax implementation
        """
        if index == self.getNumAgents(gameState):  # If current index is the same as num of agents
            index = 0  # Reset index
            depth += 1  # Increment the depth
            if depth == self.getTreeDepth():  # If current depth same as tree depth
                return self.getEvaluationFunction(gameState)

        legalActions = gameState.getLegalActions(index)
        if len(legalActions) == 0:  # If there are no actions left
            return self.getEvaluationFunction(gameState)

        scores = [(self.minimax(gameState.generateSuccessor(index, action),
            index + 1, depth)) for action in legalActions]

        if index == 0:
            return max(scores)
        else:
            return min(scores)

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using
        """
        legalActions = gameState.getLegalActions(0)
        # successors = self.generateSuccessor(gameState, legalActions)

        scores = [(self.minimax(gameState.generateSuccessor(0, action), 1, 0), action)
        for action in legalActions]

        scores = []
        for legalAction in gameState.getLegalActions(0):
            result = self.minimax(gameState.generateSuccessor(0, legalAction), 1, 0)
            scores.append((result, legalAction))
        bestScore = max(scores)[0]
        bestScores = [score[1] for score in scores if score[0] == bestScore]
        chosenIndex = random.choice(bestScores)  # Pick randomly among the best.
        return chosenIndex


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getTreeDepth(self):
        return self._treeDepth

    def getEvaluationFunction(self, gameState):
        return self._evaluationFunction((gameState))

    def getNumAgents(self, gameState):
        return gameState.getNumAgents()

    def generateSuccessor(self, gameState, legalActions):
        """
        Get the successor game state after an agent takes an action.
        """
        successors = []
        for actions in legalActions:
            action = gameState.generatePacmanSuccessor(actions)
            successors.append(action)
        return successors

    def alphaBeta(self, gameState, alpha, beta, index, depth):
        if index == self.getNumAgents(gameState):  # If current index is the same as num of agents
            index = 0  # Reset index
            depth += 1  # Increment the depth
            if depth == self.getTreeDepth():  # If current depth same as tree depth
                return (self.getEvaluationFunction(gameState), alpha, beta)
        scores = []
        legalActions = gameState.getLegalActions(index)
        if len(legalActions) == 0:
            return (self.getEvaluationFunction(gameState), alpha, beta)
        for action in legalActions:  # Iterate through all actions
            result = self.alphaBeta(gameState.generateSuccessor(index, action),
            alpha, beta, index + 1, depth)
            if index == 0:  # If index is reset value
                if result[0] >= beta:  # If initial state value is greater than beta
                    return (result[0], alpha, beta)
                alpha = max(result[0], alpha)  # Set alpha value between the max
            else:
                if result[0] <= alpha:  # If initial state value is less than alpha
                    return (result[0], alpha, beta)
                beta = max(result[0], beta)  # Set beta value between the min
            scores.append(result[0])
            alpha, beta = result[1], result[2]  # Set alpha and beta of its new traversed values

            if index == 0:  # If index is reset value
                return (max(scores), alpha, beta)
            else:
                return (min(scores), alpha, beta)

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using
        `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
        and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
        """
        scores = []
        alpha, beta = float('-inf'), float('inf')  # Initial alpha and beta values
        for legalAction in gameState.getLegalActions(0):  # For all actions
            result = self.alphaBeta(gameState.generateSuccessor(0, legalAction), alpha, beta, 1, 0)
            scores.append((result[0], legalAction))
            # print("result ", result)
            alpha, beta = result[1], result[2]
        bestScore = max(scores)[0]
        bestScores = [score[1] for score in scores if score[0] == bestScore]
        chosenIndex = random.choice(bestScores)  # Pick randomly among the best.
        return chosenIndex

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getTreeDepth(self, gameState):
        return self._treeDepth

    def getEvaluationFunction(self, gameState):
        return self._evaluationFunction((gameState))

    def getNumAgents(self, gameState):
        return gameState.getNumAgents()

    def generateSuccessor(self, gameState, legalActions):
        """
        Get the successor game state after an agent takes an action.
        """
        successors = []
        for actions in legalActions:
            action = gameState.generatePacmanSuccessor(actions)
            successors.append(action)
        return successors

    def expectimax(self, gameState, index, depth):
        if index == self.getNumAgents(gameState):  # If current index is the same as num of agents
            index = 0  # Reset index
            depth += 1  # Increment the depth
            if depth == self.getTreeDepth(gameState):  # If current depth same as tree depth
                return self.getEvaluationFunction(gameState)
        scores = []
        legalActions = gameState.getLegalActions(index)
        if len(legalActions) == 0:  # If there are no actions left
            return self.getEvaluationFunction(gameState)
        for action in legalActions:  # Iterate through all actions
            result = self.expectimax(gameState.generateSuccessor(index, action), index + 1, depth)
            scores.append(result)

        if index == 0:
            return max(scores)
        else:
            return sum(scores) / len(scores)  # min(scores)

    def getAction(self, gameState):
        """
        Returns the expectimax action from the current gameState using
        `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
        and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
        """
        scores = []
        for legalAction in gameState.getLegalActions(0):
            result = self.expectimax(gameState.generateSuccessor(0, legalAction), 1, 0)
            scores.append((result, legalAction))
        bestScore = max(scores)[0]
        bestScores = [score[1] for score in scores if score[0] == bestScore]
        chosenIndex = random.choice(bestScores)  # Pick randomly among the best.
        return chosenIndex

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """

    newScore = 0
    newPosition = currentGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()

    # Heuristics for ghosts
    ghostDistances = [ghostState.getPosition() for ghostState in newGhostStates]

    ghostScore = 0
    for ghostDistance in ghostDistances:  # For all positions of ghosts
        # If currently it is not in proximity danger
        if newGhostStates[ghostDistances.index(ghostDistance)].getScaredTimer == 0:
            ghostScore -= 25  # Penalize to incenstivise
        else:
            ghostScore = 10

    if len(oldFood.asList()) > 0:  # If there is still food left, penalize
        newScore -= distance.manhattan(newPosition, oldFood[0])
    return currentGameState.getScore() + newScore + ghostScore  # Final evaluation score

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)
