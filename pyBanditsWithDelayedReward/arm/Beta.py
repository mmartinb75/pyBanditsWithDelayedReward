# -*- coding: utf-8 -*-
'''Gaussian distributed arm.'''

__author__ = "Olivier Cappé, Aurélien Garivier"
__version__ = "$Revision: 1.4 $"

import random as rand
from Arm import Arm


class BetaReward(Arm):
    """Beta distributed arm."""
    def __init__(self, mu, sigma):
        self.sigma = sigma
        self.mu=mu
        self.expectation = mu
        self.t = 0
        self.a = ((1-self.mu)/self.sigma**2 - 1/self.mu)*self.mu**2
        self.b = self.a*(1/self.mu - 1)

    def draw(self):
        res = rand.betavariate(self.a, self.b)
        self.t +=1
        return res

    def restart(self):
        self.t = 0


