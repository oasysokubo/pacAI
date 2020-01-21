from pacai.agents.learning.reinforcement import ReinforcementAgent
from pacai.util import reflection, counter, probability
import random
import sys

class QLearningAgent(ReinforcementAgent):
    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

        # You can initialize Q-values here.
        self.qvalues = counter.Counter()

    def getAction(self, state):
        cond = probability.flipCoin(1 - self.getEpsilon())
        actions = self.getLegalActions(state)
        if cond:
            return self.getPolicy(state)
        else:
            ret = random.choice(actions)
            return ret

    def update(self, state, action, nextState, reward):
        discount = self.getDiscountRate()
        alpha = self.getAlpha()
        best = self.getValue(nextState)
        sample = reward + (discount * best)
        new_qval = ((1 - alpha) * self.getQValue(state, action)) + (alpha * sample)
        self.qvalues[(state, action)] = new_qval

    def getQValue(self, state, action):
        item = (state, action)
        if item not in self.qvalues:
            return 0.0

        return self.qvalues[(state, action)]

    def getValue(self, state):
        actions = self.getLegalActions(state)
        if len(actions) == 0:
            return 0.0
        best = -(sys.maxsize - 1)
        for action in actions:
            q_val = self.getQValue(state, action)
            if q_val > best:
                best = q_val

        return best

    def getPolicy(self, state):
        actions = self.getLegalActions(state)
        if len(actions) == 0:
            return None
        best = ('', -(sys.maxsize - 1))
        for action in actions:
            q_val = self.getQValue(state, action)
            if q_val > best[1]:
                best = (action, q_val)

        return best[0]

class PacmanQAgent(QLearningAgent):
    def __init__(self, index, epsilon = 0.05, gamma = 0.8, alpha = 0.2, numTraining = 0, **kwargs):
        kwargs['epsilon'] = epsilon
        kwargs['gamma'] = gamma
        kwargs['alpha'] = alpha
        kwargs['numTraining'] = numTraining

        super().__init__(index, **kwargs)

    def getAction(self, state):
        """
        Simply calls the super getAction method and then informs the parent of an action for Pacman.
        Do not change or remove this method.
        """

        action = super().getAction(state)
        self.doAction(state, action)

        return action

class ApproximateQAgent(PacmanQAgent):
    def __init__(self, index,
            extractor = 'pacai.core.featureExtractors.IdentityExtractor', **kwargs):
        super().__init__(index, **kwargs)
        self.featExtractor = reflection.qualifiedImport(extractor)

        # You might want to initialize weights here.
        self.weights = counter.Counter()

    def final(self, state):
        """
        Called at the end of each game.
        """

        # Call the super-class final method.
        super().final(state)

        # Did we finish training?
        if self.episodesSoFar == self.numTraining:
            # You might want to print your weights here for debugging.
            # *** Your Code Here ***
            pass

    def getQValue(self, state, action):
        q_val = 0.0
        features = self.featExtractor.getFeatures(self, state, action)
        for k in features:
            weight = self.weights[k]
            feature = features[k]
            q_val += weight * feature
        return q_val

    def update(self, state, action, nextState, reward):
        discount = self.getDiscountRate()
        alpha = self.getAlpha()
        value = self.getValue(nextState)
        q_val = self.getQValue(state, action)
        features = self.featExtractor.getFeatures(self, state, action)
        correction = (reward + (discount * value) - q_val)
        for elem in features:
            self.weights[elem] = self.weights[elem] + (alpha * correction) * features[elem]
