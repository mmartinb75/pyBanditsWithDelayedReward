# -*- coding: utf-8 -*-
'''Generic index policy.'''

__author__ = "Olivier Cappé, Aurélien Garivier"
__version__ = "$Revision: 1.5 $"


from random import choice
import time

from Policy import *

class IndexPolicy(Policy):
    """Class that implements a generic index policy."""

#  def __init__(self):

#  def computeIndex(self, arm):

    def choice(self):
        """In an index policy, choose at random an arm with maximal index."""
        #init_time = time.time()
        index = dict()
        for arm in range(self.nbArms):
            index[arm] = self.computeIndex(arm)
        maxIndex = max (index.values())
        bestArms = [arm for arm in index.keys() if index[arm] == maxIndex]
        #elapsed_time = (time.time() - init_time)*1000
        #print("elapsed_time: " + str(elapsed_time))
        return choice(bestArms)
