# -*- coding: utf-8 -*-
'''Poisson distributed arm.'''

__author__ = "Olivier Cappé, Aurélien Garivier"
__version__ = "$Revision: 1.6 $"

from scipy.stats import poisson
from math import isinf, exp
from random import random, seed

from Arm import Arm


class Poisson(Arm):
    """Poisson distributed arm, possibly truncated."""

    def __init__(self, p, trunc=float('inf'), r_seed=1, samples=10000):
        self.r_seed = r_seed
        seed(self.r_seed)
        self.p = p
        self.trunc = trunc
        self.t = 0
        # self.advance = [min(poisson.rvs(self.p), self.trunc) for i in range(samples) ]
        if isinf(trunc):
            self.expectation = p
        else:
            q = exp(-p)
            sq = q
            self.expectation = 0
            for k in range(1, self.trunc):
                q = q * p / k
                self.expectation += k * q
                sq += q
            self.expectation += self.trunc * (1 - sq)

    def draw(self):
        # res = self.advance[self.t]
        res = min(poisson.rvs(self.p), self.trunc)
        self.t += 1
        return res

    def restart(self):
        self.t = 0
        seed(self.r_seed)
