# -*- coding: utf-8 -*-
'''Delays generation for batch architecture where delay and reward are dependent'''

__author__ = "Miguel Martin, Antonio Jimenez, Alfonso Mateos"
__version__ = "1.0"

from math import isinf, exp, log
from random import random, seed

class Delayed_DR_ConfBatchPoisson:

    def __init__(self,  avg_ratio, windows_time=24,  trunc=480, r_seed=1):
        self.r_seed = r_seed
        self.windows_time = windows_time
        seed(self.r_seed)
        self.trunc = trunc
        self.avg_ratio = avg_ratio

    def getDelayedReward(self, reward, t):

        window_24_h = 3600*24
        next_batch = window_24_h - (t % window_24_h)
        p = self.avg_ratio
        c_delay = min(-1. / p * log(random()), self.trunc)

        return reward*c_delay/self.trunc, next_batch

    def restart(self):
        seed(self.r_seed)






