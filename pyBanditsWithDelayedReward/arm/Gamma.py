# -*- coding: utf-8 -*-
'''Gaussian distributed arm.'''

__author__ = "Olivier Cappé, Aurélien Garivier"
__version__ = "$Revision: 1.4 $"

import random as rand
from Arm import Arm
from random import seed

class Gamma(Arm):
    """Gaussian distributed arm."""
    def __init__(self, a, r_seed=1200021, samples=10000):
        self.r_seed = r_seed
        self.a = a
        self.t = 0
        seed(self.r_seed)
        self.advance = [min(rand.gammavariate(a[0],a[1]), 10) for i in range(samples)]
        self.expectation = sum(self.advance)/len(self.advance)
    def draw(self):
        res = self.advance[self.t]
        self.t +=1
        return res

    def restart(self):
    	self.t = 0