# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        i = 0
        while i < self.iterations:
            curValues = self.values.copy()
            for s in states:
                qvalues = []
                for action in self.mdp.getPossibleActions(s):
                    qvalues.append(self.getQValue(s, action))
                if qvalues:
                    curValues[s] = max(qvalues)
                else:
                    curValues[s] = 0
            self.values = curValues
            i += 1

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        direcitonProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        qvalue = sum([p * (self.mdp.getReward(state, action, nextState) + self.discount * self.getValue(nextState)) for nextState, p in direcitonProbs])
        # qvalue = 0
        # for t in direcitonProbs:
        #     nextState, nextStateP = t
        #     qvalue += nextStateP * (self.mdp.getReward(state, action, nextState) + self.discount * self.getValue(nextState))
        return qvalue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None
        else:
            return max([(self.getQValue(state, a), a) for a in self.mdp.getPossibleActions(state)])[1]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        i = 0
        while i < self.iterations:
            curValues = self.values.copy()
            currState = states[i % len(states)]
            qvalues = []
            for action in self.mdp.getPossibleActions(currState):
                qvalues.append(self.getQValue(currState, action))
            if qvalues:
                self.values[currState] = max(qvalues)
            else:
                self.values[currState] = 0
            i += 1

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        mdp = self.mdp
        values = self.values
        discount = self.discount
        iterations = self.iterations
        theta = self.theta

        states = self.mdp.getStates()
        predecessors = {}
        diffQ = util.PriorityQueue()

        # init the predecessors to a dict with sets
        for state in states:
            predecessors[state] = set()

        for state in states:
            qvalue = []
            for action in self.mdp.getPossibleActions(state):
                for t in self.mdp.getTransitionStatesAndProbs(state, action):
                    if t[1] != 0.0:
                        predecessors[t[0]].add(state)
                qvalue.append(self.getQValue(state, action))

            if not mdp.isTerminal(state):
                maxq = max(qvalue)
                diff = abs(self.values[state] - maxq)
                diffQ.update(state, -diff)

        i = 0
        while i < self.iterations:
            if diffQ.isEmpty():
                break

            state = diffQ.pop()
            if not self.mdp.isTerminal(state):
                qvalue = [self.getQValue(state, action) for action in self.mdp.getPossibleActions(state)]
                self.values[state] = max(qvalue)

            for pstate in predecessors[state]:
                pstateQvalue = [self.getQValue(pstate, action) for action in self.mdp.getPossibleActions(pstate)]
                maxq = max(pstateQvalue)
                diff = abs(values[pstate] - maxq)
                if diff > theta:
                    diffQ.update(pstate, -diff)
            i += 1 