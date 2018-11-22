# -*- coding: utf-8 -*-
'''Bernoulli distributed arm.'''

__author__ = "Miguel Martin, Antonio Jimenez, Alfonso Mateos"
__version__ = "1.0"

from random import random, seed
from Arm import Arm
from math import isinf, exp, log
import numpy as np


class Bernoulli_Delay(Arm):
    """Bernoulli distributed arm."""

    def __init__(self, p, delay_ratio, r_seed=1, trunc=480, samples=1000000):
        self.r_seed = r_seed
        seed(self.r_seed)
        self.p = p
        self.trunc = trunc

        self.t = 0
        self.delay_ratio = delay_ratio
        self.advance = [float(random() < self.p)*min(-1. / self.delay_ratio * log(random()), self.trunc)/self.trunc
                        for _ in range(samples)]
        self.expectation = np.mean(self.advance)
        print(self.expectation)
        print(np.var(self.advance))

    def draw(self):
        res = self.advance[self.t]
        self.t += 1
        return res

    def restart(self):
        self.t = 0
        seed(self.r_seed)
