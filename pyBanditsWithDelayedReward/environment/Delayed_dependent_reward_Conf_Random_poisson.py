# -*- coding: utf-8 -*-
'''Delays generation for online architecture where delay and reward are dependent'''

__author__ = "Miguel Martin, Antonio Jimenez, Alfonso Mateos"
__version__ = "1.0"


from math import isinf, exp, log
from random import random, seed

class Delayed_DR_Conf_Random_poisson:

    def __init__(self,  avg_ratio, trunc=200, r_seed=1):
        self.r_seed = r_seed
        self.trunc = trunc
        self.avg_ratio = avg_ratio
        seed(self.r_seed)

    def getDelayedReward(self, reward, t):
        p = self.avg_ratio
        c_delay = min(-1. / p * log(random()), self.trunc)
        return reward*c_delay/self.trunc,  c_delay

    def restart(self):
        seed(self.r_seed)






