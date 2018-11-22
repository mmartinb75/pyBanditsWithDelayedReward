# -*- coding: utf-8 -*-
'''Delays generation for batch architecture'''

__author__ = "Miguel Martin, Antonio Jimenez, Alfonso Mateos"
__version__ = "1.0"

from scipy.stats import poisson

class DelayedConfBatchPoisson:

    def __init__(self,  windows_time_hours=24):
        self.windows_time_hours = windows_time_hours

    def getDelayedReward(self, reward, t):
        window_24_h = 3600*self.windows_time_hours
        next_batch = window_24_h - (t % window_24_h)

        return reward, next_batch

    def restart(self):
        pass







