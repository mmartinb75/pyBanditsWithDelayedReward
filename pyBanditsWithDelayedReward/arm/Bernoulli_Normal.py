# -*- coding: utf-8 -*-
'''Bernoulli distributed arm.'''

__author__ = "Olivier Cappé, Aurélien Garivier"
__version__ = "$Revision: 1.6 $"

from random import random, seed, gauss
from Arm import Arm
import numpy as np


class Bernoulli_Normal(Arm):
    """Bernoulli distributed arm."""

    def __init__(self, p, trunc=float('inf'), r_seed=1, mu=0.5, sigma=0.5, samples=1000000):
        self.r_seed = r_seed
        seed(self.r_seed)
        self.trunc = trunc
        self.p = p
        self.t = 0
        self.mu = mu
        self.sigma = sigma
        self.advance = [float(max(0, min(self.trunc, self.mu+self.sigma*gauss(0, 1))) if random() < self.p else 0) for i in range(samples)]
        seed(self.r_seed)
        self.expectation = np.mean(self.advance, 0)
        print self.expectation
    def draw(self):
        # res = self.advance[self.t]
        res = float(max(0, min(self.trunc, self.mu+self.sigma*gauss(0, 1))) if random() < self.p else 0)
        self.t += 1
        return res

    def restart(self):
        self.t = 0
        seed(self.r_seed)
