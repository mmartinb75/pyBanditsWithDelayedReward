# -*- coding: utf-8 -*-
'''The PR2 Policy of possibilistic reward family.
  Reference: [M. Martín, A. Jiménez & A. Mateos, Neurocomputing, 2018].'''

__author__ = "Miguel Martin, Antonio Jimenez, Alfonso Mateos"
__version__ = "1.0"


from math import sqrt, log, exp
import random as rand


from IndexPolicy import IndexPolicy

class PossibilisticReward_chernoff2(IndexPolicy):
    """Class that implements the PR2 policy.
    """

    def __init__(self, nbArms, amplitude=1., lower=0., scale=1):
        self.nbArms = nbArms
        self.factor = amplitude
        self.amplitude = 1
        self.lower = lower
        self.nbDraws = dict()
        self.cumReward = dict()
        self.cumReward2 = dict()
        self.scale = scale

    def startGame(self):
        self.t = 1
        for arm in range(self.nbArms):
            self.nbDraws[arm] = 0
            self.cumReward[arm] = 0.0
            self.cumReward2[arm] = 0.0

    def computeIndex(self, arm):
        if self.nbDraws[arm] < 1:
            return rand.betavariate(1, 1)*self.factor
        else:
            mu1 = self.cumReward[arm]/self.nbDraws[arm]
            mu = mu1/self.factor
            s = self.nbDraws[arm]
            a = mu*s
            b = s - a
            bet = rand.betavariate(1+a, 1+b)
            return bet


    def getReward(self, arm, reward):
        self.nbDraws[arm] += 1
        self.cumReward[arm] += reward
        self.cumReward2[arm] += self.cumReward[arm]**2
        self.t += 1

