# -*- coding: utf-8 -*-
'''Blackbox wrapper to aply any Bandit method to improve performancen under delayed feedback
  Reference: [P.Joulani, A.Gyorgy & C.Szepesvari - Conf. on Machine Learning, 2013].'''

__author__ = "Miguel Martin"
__version__ = "$Revision: 1.0"

from math import log
from random import choice

import kullback
from IndexPolicy import IndexPolicy
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class BlackBox(IndexPolicy):


    def __init__(self, nbArms, policy, amplitude=1., lower=0.):
        self.nbArms = nbArms
        self.amplitude = amplitude
        self.lower = lower
        self.nbDraws = dict()
        self.cumReward = dict()
        self.type = type
        self.max_mean = 0
        self.pending_arms = list()
        self.new_arms = list()
        self.policy = policy
        self.rewards_queue = dict()
        self.arm_chosen = 0

    def startGame(self):
        self.t = 1
        self.pending_arms = [i for i in range(self.nbArms)]
        self.new_arms = []
        for arm in range(self.nbArms):
            self.nbDraws[arm] = 0
            self.cumReward[arm] = 0.0
            self.rewards_queue[arm] = Queue()
        self.policy.startGame()

        self.arm_chosen = choice(range(self.nbArms))

    def computeIndex(self, arm):
        return self.policy.computeIndex(arm)

    def choice(self):
        """In an index policy, choose at random an arm with maximal index."""
        while not self.rewards_queue[self.arm_chosen].isEmpty():
            r = self.rewards_queue[self.arm_chosen].dequeue()
            self.inner_reward(self.arm_chosen, r)
            self.arm_chosen = self.inner_choice()

        return self.arm_chosen

    def inner_choice(self):
        index = dict()
        for arm in range(self.nbArms):
            index[arm] = self.computeIndex(arm)
        maxIndex = max(index.values())
        bestArms = [arm for arm in index.keys() if index[arm] == maxIndex]
        return choice(bestArms)

    def inner_reward(self, arm, reward):
        self.policy.getReward(arm, reward)

    def getReward(self, arm, reward):

        self.nbDraws[arm] += 1
        self.cumReward[arm] += (reward - self.lower) / self.amplitude
        self.t += 1

        self.rewards_queue[arm].enqueue(reward)




     # Debugging code
        # print "arm " + str(arm) + " receives " + str(reward)
        # print str(self.nbDraws[arm]) + " " + str(self.cumReward[arm])
