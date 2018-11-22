# -*- coding: utf-8 -*-

'''Non Homogeneous poisson process implementation'''

__author__ = "Miguel Martin, Antonio Jimenez, Alfonso Mateos"
__version__ = "1.0"

from arm import Exponential
from math import isinf, exp, log
from random import random, seed


class NHPoissonProcess:

    def __init__(self, ratio_function, trunc=3600, r_seed=1):
        self.ratio_function = ratio_function
        self.r_seed = r_seed
        self.trunc = trunc

    def draw(self, t):
        p = self.ratio_function(t)
        res = min(-1. / p * log(random()), self.trunc)
        return res

    def reset(self):
        seed(self.r_seed)


def generate_ratio_function(bias, params):
    def arrive_ratio(x):
        cum_bias = bias
        for low, up, pte in params:
            if low <= x < up:
                return (x-low)*pte + cum_bias
            cum_bias += (up-low)*pte
            last_up = up

        #last segment:
        return (bias - cum_bias)/(24-last_up)*(x-last_up) + cum_bias
    return arrive_ratio


def generate_ratio_function(params):
    def arrive_ratio(x):
        x = x % 24
        last_x_param = 0
        last_y_param = 0
        for x_param, y_param in params:
            if last_x_param <= x < x_param:
                pte = (y_param - last_y_param)/(x_param - last_x_param)
                return (x-last_x_param)*pte + last_y_param

            last_x_param = x_param
            last_y_param = y_param

        return (params[0][1] - last_y_param)/(24-last_x_param)*(x-last_x_param) + last_y_param

    return arrive_ratio
