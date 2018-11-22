# -*- coding: utf-8 -*-
'''Utility class for handling the results of a Multi-armed Bandits experiment.'''

__author__ = "Olivier Cappé, Aurélien Garivier"
__version__ = "$Revision: 1.7 $"


import numpy as np

class Result:
    """The Result class for analyzing the output of bandit experiments."""
    def __init__(self, nbArms, horizon):
        self.nbArms = nbArms
        self.choices = np.zeros(horizon)
        self.rewards = np.zeros(horizon)
        self.vars = np.zeros(horizon)
        self.bads = np.zeros(horizon)
        self.nbDraws = dict()
        self.worst = np.zeros(horizon)
        self.nbEvents = 0

        for arm in range(self.nbArms):
            self.nbDraws[arm] = 0

    def store(self, t, choice, reward):
        self.choices[t] = choice
        self.rewards[t] = reward
        self.nbDraws[choice] += 1
        self.nbEvents +=1

    def getNbPulls(self):
        if (self.nbArms==float('inf')):
            self.nbPulls=np.array([])
            pass
        else :
            nbPulls = np.zeros(self.nbArms)
            for choice in self.choices:
                nbPulls[int(choice)] += 1
            return nbPulls
    
    def bestExpect(self):
        self.armsExp = np.zeros(self.nbArms)
        self.armsTimes = np.zeros(self.nbArms)
        for i in self.choices:
            self.armsExp[self.choices[i]] += self.rewards[i]
            self.armsTimes[self.choices[i]] += 1

        return max([self.armsExp[k]/self.armsTimes[k] for k in range(self.nbArms)])

    def getRegret(self, bestExpectation):
        return np.cumsum(bestExpectation-self.rewards)
