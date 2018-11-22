# -*- coding: utf-8 -*-
'''The generic kl-UCB policy for one-parameter exponential distributions.
  Reference: [Garivier & cappé - COLT, 2011].'''

__author__ = "Miguel Martin"
__version__ = "$Revision: 1.0"

from math import log

import kullback
from IndexPolicy import IndexPolicy


class DMED(IndexPolicy):
    """The generic DMED policy for one-parameter exponential distributions.
      """

    def __init__(self, nbArms, amplitude=1., lower=0.):
        self.nbArms = nbArms
        self.amplitude = amplitude
        self.lower = lower
        self.nbDraws = dict()
        self.cumReward = dict()
        self.type = type
        self.max_mean = 0
        self.pending_arms = list()
        self.new_arms = list()

    def startGame(self):
        self.t = 1
        self.pending_arms = [i for i in range(self.nbArms)]
        self.new_arms = []
        for arm in range(self.nbArms):
            self.nbDraws[arm] = 0
            self.cumReward[arm] = 0.0

    def computeIndex(self, arm):
        if len(self.pending_arms) > 0 and arm in self.pending_arms:
            return self.pending_arms.index(arm) + 1
        else:
            return 0


    def getReward(self, arm, reward):
        k = kullback.klBern

        self.nbDraws[arm] += 1
        self.cumReward[arm] += (reward - self.lower) / self.amplitude
        self.t += 1


        if self.pending_arms.__contains__(arm):
            self.pending_arms.remove(arm)
        self.max_mean = max([self.cumReward[i]/self.nbDraws[i] if self.nbDraws[i] != 0 else 0 for i in range(self.nbArms)])
        for arm in range(self.nbArms):
            test1 = arm not in self.pending_arms
            test2 = arm not in self.new_arms
            mean = self.cumReward[arm]/self.nbDraws[arm] if self.nbDraws[arm] != 0 else 0
            times = self.t/self.nbDraws[arm] if self.nbDraws[arm] != 0 else 1
            test3 = self.nbDraws[arm]*k(mean,self.max_mean) <= log(times)
            if test1 and test2 and test3:
                self.new_arms.append(arm)

        if len(self.pending_arms) == 0:
            self.pending_arms = self.new_arms
            self.new_arms = []



     # Debugging code
        # print "arm " + str(arm) + " receives " + str(reward)
        # print str(self.nbDraws[arm]) + " " + str(self.cumReward[arm])
