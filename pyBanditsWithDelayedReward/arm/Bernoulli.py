# -*- coding: utf-8 -*-
'''Bernoulli distributed arm.'''

__author__ = "Olivier Cappé, Aurélien Garivier"
__version__ = "$Revision: 1.6 $"

from random import random, seed
from Arm import Arm


class Bernoulli(Arm):
    """Bernoulli distributed arm."""

    def __init__(self, p, r_seed=1, samples=10000):
        self.r_seed = r_seed
        seed(self.r_seed)
        self.p = p
        self.expectation = p
        self.t = 0
        # self.advance = [float(random()<self.p) for i in range(samples)]

    def draw(self):
        # res = self.advance[self.t]
        res = float(random() < self.p)
        self.t += 1
        return res

    def restart(self):
        self.t = 0
        seed(self.r_seed)
