import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent

from pacai.core import distance
import pacai.util.reflection as reflection

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
        if action == 0:
            return 0

        newScore = successorGameState.getScore()
        newPosition = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        ghostable = []
        for ghostState in newGhostStates:
            ghostPosition = ghostState.getPosition()

            print("ghost position: ", ghostPosition)
            print("new scared times: ", newScaredTimes)
            ghostable.append((ghostPosition[0], ghostPosition[1]))
            ghostable.append((ghostPosition[0], ghostPosition[1] - 1))
            ghostable.append((ghostPosition[0], ghostPosition[1] + 1))
            ghostable.append((ghostPosition[0] - 1, ghostPosition[1]))
            ghostable.append((ghostPosition[0] + 1, ghostPosition[1]))
        

        if newPosition in ghostable:
            newScore -= 500
        if len(newFood) > 0:
            print(newFood.asList())
            newScore -= distance.manhattan(newPosition, newFood[0])
        if len(newFood.asList()) < len(oldFood.asList()):
            newScore = 0
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

    # def __init__(self, index, depth = 2):
    #     self.index = 0
    #     self._treeDepth = int(depth)
    #     self.currentDepth = int(currentDepth)
    #     self._evaluationFunction = reflection.qualifiedImport(evalFn='pacai.core.eval.score)

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
        if index == gameState.getNumAgents():
            index = 0
            depth += 1
            if depth == self.getTreeDepth():
                return self.getEvaluationFunction(gameState)

        scores = []
        legalActions = gameState.getLegalActions(index)
        if len(legalActions) == 0:
            return self.getEvaluationFunction(gameState)
        for action in legalActions:
            scores.append(self.minimax(gameState.generateSuccessor(index, action), index + 1, depth)) 

        if index == 0:
            return max(scores)
        else:
            return min(scores)


    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using
        """
        legalActions = gameState.getLegalActions(0)
        successors = self.generateSuccessor(gameState, legalActions)

        scores = [(self.minimax(gameState.generateSuccessor(0, action), 1, 0), action) for action in legalActions]

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

    def getTreeDepth(self, gameState):
        return self._treeDepth

    def getEvaluationFunction(self, gameState):
        return self._evaluationFunction((gameState))

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
        if index == gameState.getNumAgents():
            index = 0
            depth += 1
            if depth == self.getTreeDepth(gameState):
                return (self.getEvaluationFunction(gameState), alpha, beta)
        
        scores = []
        legalActions = gameState.getLegalActions(index)
        if len(legalActions) == 0:
            return (self.getEvaluationFunction(gameState), alpha, beta)
        
        for action in legalActions:
            result = self.alphaBeta(gameState.generateSuccessor(index, action), alpha, beta, index + 1, depth)
            if index == 0:
                if result[0] >= beta:
                    return (result[0], alpha, beta)
                alpha = max(result[0], alpha)
            else:
                if result[0] <= alpha:
                    return (result[0], alpha, beta)
                beta = min(result[0], beta)
            scores.append(result[0])
            alpha, beta = result[1], result[2]
            if index == 0:
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
        alpha, beta = float('-inf'), float('inf') 
        for legalAction in gameState.getLegalActions(0):
            print(legalAction)
            print("pass")
            result = self.alphaBeta(gameState.generateSuccessor(0, legalAction), alpha, beta, 1, 0)
            print(result)
            print("pass2")
            scores.append((result[0], legalAction))
            alpha, beta = result[1], result[2]
        bestScore = max(scores)[0]
        print(bestScore)
        print("pass3")
        bestScores = [score[1] for score in scores if score[0] == bestScore]
        print("pass4")
        print(bestScores)
        chosenIndex = random.choice(bestScores)  # Pick randomly among the best.
        print("pass5")
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
        if index == gameState.getNumAgents():
            index = 0
            depth += 1
            if depth == self.getTreeDepth(gameState):
                return (self.getEvaluationFunction(gameState))
        scores = []
        legalActions = gameState.getLegalActions(index)
        if len(legalActions) == 0:
            return (self.getEvaluationFunction(gameState))
        for action in legalActions:
            result = self.expectimax(gameState.generateSuccessor(index, action), index + 1, depth)
            scores.append(result)
        if index == 0:
            return max(scores)
        else:
            return sum(scores) / len(scores)

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
    newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]
    if len(oldFood.asList()) > 0:
        newScore -= distance.manhattan(newPosition, oldFood[0])
    return currentGameState.getScore() + newScore

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
