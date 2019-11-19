"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None

def question2():
    """
    [Enter a description of what you did here.]
    I reduced the noise, which in turn is the
    most significant value to enables the agent to
    move freely with less risk factor, so agent will
    not worry about cliff danger.
    """

    answerDiscount = 0.9
    answerNoise = 0.016667

    return answerDiscount, answerNoise

def question3a():
    """
    [Enter a description of what you did here.]
    Reducing the discount will give less reward to the
    agent that tries to go to a distant path.
    Reduced the noise, whihc in turn enables the agent to
    move freely with less risk factor, so agent will
    not worry about cliff danger.
    Making the living reward to negative would give less
    incentive to take the longer route because of negative
    points, so agent will take the closest route as a result.
    """

    answerDiscount = 0.4
    answerNoise = 0.016667
    answerLivingReward = -1.5

    return answerDiscount, answerNoise, answerLivingReward

def question3b():
    """
    [Enter a description of what you did here.]
    Reducing the discount will give less reward to the
    agent that tries to go to a distant path.
    A higher noise in turn makes it so the agent has
    less opportunity to move as it wants, which makes it
    less likely to go off cliff.
    Making the living reward to negative would give less
    incentive to take the longer route because of negative
    points, so agent will take the closest route as a result.
    """

    answerDiscount = 0.4
    answerNoise = 0.18
    answerLivingReward = -1.5

    return answerDiscount, answerNoise, answerLivingReward

def question3c():
    """
    [Enter a description of what you did here.]
    A higher discount will give more reward to the agent
    to take a more distant path.
    Reduced the noise, whihc in turn enables the agent to
    move freely with less risk factor, so agent will
    not worry about cliff danger.
    Making the living reward higher would give more
    incentive to take the longer route, so agent will
    take the longest route as a result.
    """

    answerDiscount = 0.9
    answerNoise = 0.1
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3d():
    """
    [Enter a description of what you did here.]
    A higher discount will give more reward to the agent
    to take a more distant path.
    A higher noise in turn makes it so the agent has
    less opportunity to move as it wants, which makes it
    less likely to go off cliff.
    Making the living reward higher would give more
    incentive to take the longer route, so agent will
    take the longest route as a result.
    """

    answerDiscount = 0.9
    answerNoise = 0.5
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3e():
    """
    [Enter a description of what you did here.]
    A higher discount will give more reward to the agent
    to take a more distant path.
    A higher noise in turn makes it so the agent has
    less opportunity to move as it wants, which makes it
    less likely to go off cliff.
    Making the living reward the highest so it can get
    more incentive to not go to the exit and take the
    longest path possible.
    """

    answerDiscount = 0.9
    answerNoise = 0.5
    answerLivingReward = 3.0

    return answerDiscount, answerNoise, answerLivingReward

def question6():
    """
    [Enter a description of what you did here.]
    """

    answerEpsilon = 0.3
    answerLearningRate = 0.5

    return answerEpsilon, answerLearningRate

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
