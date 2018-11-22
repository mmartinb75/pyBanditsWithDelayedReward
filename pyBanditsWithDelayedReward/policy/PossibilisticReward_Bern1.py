# -*- coding: utf-8 -*-
'''The PR3 Policy of possibilistic reward family.
  Reference: [M. Martín, A. Jiménez & A. Mateos, Neurocomputing, 2018].'''

__author__ = "Miguel Martin, Antonio Jimenez, Alfonso Mateos"
__version__ = "1.0"


from math import sqrt, log, exp
import random as rand
import numpy as np
import decimal
decimal.getcontext().prec = 100
from IndexPolicy import IndexPolicy
import time

class PossibilisticReward_Bern1(IndexPolicy):
    """Class that implements the PR3 policy.
    """

    def __init__(self, nbArms, amplitude=1., lower=0., weight=0.5, confidence=0.1):
        self.nbArms = nbArms
        self.factor = amplitude
        self.amplitude = 1
        self.lower = lower
        self.nbDraws = dict()
        self.cumReward = dict()
        self.cumReward2 = dict()
        self.sampleMeans = dict()
        self.vars = dict()
        self.outDraws = dict()
        self.var = 0
        self.Ks = dict()
        self.Exs = dict()
        self.Ex2s = dict()
        self.meansDiff = 1
        self.amplitudes = dict()
        self.confidence=confidence

        #Kurtosis:
        self.n = 0
        self.mean = 0
        self.M2 = 0
        self.M3 = 0
        self.M4 = 0
        self.kurtosis = 0

        for i in range(nbArms):
            self.outDraws[i] = np.array([])

        self.weight = weight
        print self.weight
        self.scale = 1

    def startGame(self):

        self.t = 1
        self.Ex = 0
        self.Ex2 = 0

        #Init Kurtosis:
        self.n = 0
        self.mean = 0
        self.M2 = 0
        self.M3 = 0
        self.M4 = 0
        self.amplitude = 1

        self.kurtosis = 0

        for arm in range(self.nbArms):
            self.nbDraws[arm] = 0
            self.cumReward[arm] = 0.0
            self.cumReward2[arm] = 0.0
            self.vars[arm] = 1.0
            self.Ks[arm] = 0.0
            self.Exs[arm] = 0.0
            self.Ex2s[arm] = 0.0
            self.sampleMeans[arm] = 0
            self.amplitudes[arm] = 1


    def computeIndex(self, arm):
        if self.nbDraws[arm] < 1:
            return rand.betavariate(1, 1)*self.factor
        else:
            mu1 = self.cumReward[arm]/self.nbDraws[arm]
            mu = mu1/self.factor
            s = self.nbDraws[arm]
            r = max([1, mu*(1-mu)/self.amplitudes[arm]])

            n = s*r
            a = mu*n
            b = n - a
            bet = rand.betavariate(1+a, 1+b)
            return bet

    def getReward(self, arm, reward):
        self.nbDraws[arm] += 1
        self.cumReward[arm] += reward
        self.cumReward2[arm] += float(reward)/self.factor

        norm_reward = float(reward)/self.factor
    
        # Calculate Variance
        if self.nbDraws[arm] == 1:
            self.Ks[arm] = norm_reward

        self.Exs[arm] += float(norm_reward - self.Ks[arm])
        self.Ex2s[arm] += (norm_reward - self.Ks[arm]) * (norm_reward - self.Ks[arm])

        if self.nbDraws[arm] < 2:
            var = self.Ex2s[arm] - (self.Exs[arm]*self.Exs[arm])
        else:
            den = self.nbDraws[arm]
            var = (self.Ex2s[arm] - (self.Exs[arm]*self.Exs[arm])/den) / (den-1)

        if var == 0:
            self.amplitudes[arm] = 1
        else:
            self.amplitudes[arm] = min([0.25, var + sqrt(log(self.confidence)/(-2*self.nbDraws[arm]))])
            
        self.var = var
        self.t += 1

    def getVar(self):
        return self.amplitude
