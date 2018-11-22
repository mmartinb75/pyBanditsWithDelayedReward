# -*- coding: utf-8 -*-
'''Delays generation for online architecture'''

__author__ = "Miguel Martin, Antonio Jimenez, Alfonso Mateos"
__version__ = "1.0"


from math import isinf, exp, log
from random import random, seed

class Delayed_Conf_Random_poisson:

    def __init__(self,  avg_ratio, trunc=200, r_seed=1):
        self.r_seed = r_seed
        self.trunc = trunc
        self.avg_ratio = avg_ratio
        seed(self.r_seed)

    def getDelayedReward(self, reward, t):
        p = self.avg_ratio
        res = min(-1. / p * log(random()), self.trunc)
        return reward, res

    def restart(self):
        seed(self.r_seed)






