from pacai.agents.learning.value import ValueEstimationAgent
from pacai.util import counter
import random

class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate = 0.9, iters = 100, **kwargs):
        super().__init__(index)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = counter.Counter()  # A Counter is a dict with default 0
        self.setValue()

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def setValue(self):
        # Compute the values here.
        for iter in range(self.iters):
            new_values = self.values
            for state in self.mdp.getStates():
                possible_actions = self.mdp.getPossibleActions(state)
                if not possible_actions:
                    new_values[state] = self.getValue(state)
                else:
                    # print('possible actions:', possible_actions)
                    for action in possible_actions: # Or just pick a random one
                        new_values[state] = max([self.getQValue(state, action)])
                        print('possible state', new_values[state])
                self.values = new_values

    def getQValue(self, state, action):
        """
        returns the q-value of the (state, action) pair
        """
        transitions = self.mdp.getTransitionStatesAndProbs(state, action)
        return sum(
            [
                transition[1] *
                (self.discountRate * self.getValue(transition[0]) +
                self.mdp.getReward(state, action, transition[0])) for transition in transitions 
            ])

    def getPolicy(self, state):
        """
        What is the best action to take in the state?
        Note that because we might want to explore,
        this might not coincide with `ValueEstimationAgent.getAction`.
        Concretely, this is given by:
        ```
        policy(state) = arg_max_{action in actions} Q(state, action)
        ```
        If many actions achieve the maximal Q-value,
        it doesn't matter which is selected.
        """

        if self.mdp.isTerminal(state):
            return None

        possible_actions = self.mdp.getPossibleActions(state)

        q_values = []
        for action in possible_actions:
            # print('PASS')
            transitions = self.mdp.getTransitionStatesAndProbs(state, action)
            q_value = sum([
                transition[1] *
                (self.discountRate * self.getValue(transition[0]) +
                self.mdp.getReward(state, action, transition[0])) for transition in transitions]
                )
            # print('q_val: ', q_value)
            q_values.append(q_value)
        bestScore = max(q_values)
        bestIndices = [index for index in range(len(q_values)) if q_values[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return possible_actions[chosenIndex]


    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """
        return self.getPolicy(state)

    def loadAgent(name, index, args={}):
        pass

    def final(self, state):
        pass