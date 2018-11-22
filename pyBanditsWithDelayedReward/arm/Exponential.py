# -*- coding: utf-8 -*-
'''Exponentially distributed arm.'''

__author__ = "Olivier Cappé, Aurélien Garivier"
__version__ = "$Revision: 1.5 $"

from math import isinf, exp, log
from random import random, seed

import numpy as np

from Arm import Arm


class Exponential(Arm):
    """Exponentially distributed arm, possibly truncated"""

    def __init__(self, p, trunc=float('inf'), r_seed=1, samples=100000):
        self.r_seed = r_seed
        self.p = p
        self.trunc = trunc
        self.t = 0
        a = float(1)
        seed(self.r_seed)
        self.advance = [min(-1. / self.p * log(random()), self.trunc) for i in range(samples)]
        if isinf(trunc):
            self.expectation = 1. / p
        else:
            self.expectation = (1. - exp(-p * trunc)) / p

        self.expectation2 = sum(self.advance) / len(self.advance)

    def draw(self):

        #res = self.advance[self.t]
        res = min(-1. / self.p * log(random()), self.trunc)
        self.t += 1
        return res

    def restart(self):
        self.t = 0
        seed(self.r_seed)
