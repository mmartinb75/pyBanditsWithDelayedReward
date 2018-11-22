# -*- coding: utf-8 -*-
'''The BESA policy.
 Reference: [A. Baransi, O.A. Maillard, S. Mannor, in: Proc. Eur. Conf. Machine Learning, 2014]'''

__author__ = "Miguel Martin"
__version__ = "1.0"

import numpy

from math import sqrt, log, exp
import random as rand

from IndexPolicy import IndexPolicy
from functools import cmp_to_key
from numpy import *

def winBesa(arm1, arm2):
    la1 = len(arm1)
    la2 = len(arm2)
    if la1 == 0 and la2 == 0:
        return rand.choice([1, -1])
    if la1 == 0:
        return 1
    if la2 == 0:
        return -1

    if la1 <= la2:
        truncate_list = rand.sample(arm2, la1)
        # truncate_list = []
        # for i in range(la1):
        #     truncate_list += [rand.choice(arm2)]

        sample_mean_arm1 = float(mean(arm1))
        sample_mean_arm2 = float(mean(truncate_list))

    else:
        truncate_list = rand.sample(arm1, la2)
        # truncate_list = []
        # for i in range(la2):
        #     truncate_list += [rand.choice(arm1)]

        sample_mean_arm1 = float(mean(truncate_list))
        sample_mean_arm2 = float(mean(arm2))

        #print "arms: " + str(arm1) + ":" + str(arm2)
        #print "length arms: " + str(la1) + ":" + str(la2)
        #print "means: " + str(sample_mean_arm1) + ":" + str(sample_mean_arm2)



    result = sample_mean_arm1 - sample_mean_arm2

    if (result == 0) and (la1 == la2):
        #return rand.choice([1, -1])
        return 0

    if (result == 0) and (la1 < la2):
        return 1

    if result == 0:
        return -1

    return result



class besa(IndexPolicy):
    """Class that implements the besa policy.
    """

    def __init__(self, nbArms, amplitude=1., lower=0., scale=1):
        self.nbArms = nbArms
        self.amplitude = amplitude
        self.lower = lower
        self.nbDraws = dict()
        self.cumReward = dict()
        self.cumReward2 = dict()
        self.scale = scale
        self.secuence = dict()
        self.sortedArms = list()


    def startGame(self):
        self.t = 1
        self.sortedArms = list()
        for arm in range(self.nbArms):
            self.nbDraws[arm] = 0
            self.cumReward[arm] = 0.0
            self.cumReward2[arm] = 0.0
            self.secuence[arm] = list()
            self.sortedArms.append(self.secuence[arm])



    def computeIndex(self, arm):
        if arm == 0:
            self.needIndexUpdate = False
            self.sortedArms = sorted(self.sortedArms, key=cmp_to_key(winBesa), reverse=True)

        return (self.nbArms - self.sortedArms.index(self.secuence[arm]))



    def getReward(self, arm, reward):
        self.nbDraws[arm] += 1
        self.cumReward[arm] += reward
        self.cumReward2[arm] += reward**2
        self.secuence[arm].append(reward)
        #print "Before sorted: " + str(self.sortedArms)
        #print "sorted: " + str(self.sortedArms)
        self.t += 1

