# -*- coding: utf-8 -*-
'''Gaussian distributed arm.'''

__author__ = "Olivier Cappé, Aurélien Garivier"
__version__ = "$Revision: 1.4 $"

import random as rand
from Arm import Arm


class Gaussian(Arm):
    """Gaussian distributed arm."""
    def __init__(self, mu, sigma):
        self.sigma = sigma
        self.mu=mu
        self.expectation = mu
        self.t = 0
        self.advance = [self.mu+self.sigma*rand.gauss(0,1)]
    def draw(self):
        res = self.advance[self.t]
        self.t +=1
        return res

    def restart(self):
    	self.t = 0

