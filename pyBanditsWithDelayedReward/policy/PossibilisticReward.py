# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
'''The Possibilistic Policy.
  Reference: [Miguel Martin].'''

__author__ = "Miguel Martin, Antonio Jimenez, Alfonso Mateos"
__version__ = "1.0"


from math import sqrt, log, exp
import random as rand

from IndexPolicy import IndexPolicy

class PossibilisticReward(IndexPolicy):
    """Class that implements the UCB-V policy.
    """

    def __init__(self, nbArms, amplitude=1., lower=0., scale=1):
        self.nbArms = nbArms
        self.amplitude = amplitude
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

    def fuzzyTransformed(self, x, arm):
        m = self.cumReward[arm]/self.nbDraws[arm]
        s = self.nbDraws[arm]
        lowDelta = exp(-2*self.scale*s*(m/self.amplitude)**2)
        upDelta = exp(-2*self.scale*s*((m-self.amplitude)/self.amplitude)**2)
        if x == m:
            return 1
        elif  x >= self.amplitude or x <= 0:
            return 0
        elif x < m:
            return (exp(-2*self.scale*s*((m-x)/self.amplitude)**2) - lowDelta)/(1-lowDelta)
        else: 
            return (exp(-2*self.scale*s*((m-x)/self.amplitude)**2) - upDelta)/(1-upDelta)

    def fuzzy(self, x, arm):
        m = self.cumReward[arm]/self.nbDraws[arm]
        s = self.nbDraws[arm]
        return exp(-2*self.scale*s*((m-x)/self.amplitude)**2)

    def computeIndex(self, arm):
        if self.nbDraws[arm] < 1:
            return rand.random()*self.amplitude + self.lower
        else:
            mu = self.cumReward[arm]/self.nbDraws[arm]
            s = self.nbDraws[arm]
            sigma = self.amplitude/sqrt(4*s*self.scale)
            r1 = mu+sigma*rand.gauss(0,1)
            r2 = rand.random()
            while r2 > self.fuzzyTransformed(r1, arm)/self.fuzzy(r1,arm):
                r1 = mu+sigma*rand.gauss(0,1)
                r2 = rand.random()
            return r1


    def getReward(self, arm, reward):
        self.nbDraws[arm] += 1
        self.cumReward[arm] += reward
        self.cumReward2[arm] += reward**2
        self.t += 1

