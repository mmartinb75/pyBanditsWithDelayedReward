# -*- coding: utf-8 -*-
'''A utility class for evaluating the performance of a policy in multi-armed bandit problems.'''

__author__ = "Olivier Cappé, Aurélien Garivier"
__version__ = "$Revision: 1.10 $"


import numpy as np
#from translate.misc.progressbar import ProgressBar

class Evaluation:
  
    def __init__(self, env, pol, nbRepetitions, max_decisions, horizon, tsav=[]):
        print("tsav " + str(tsav))
        print("max_dec:" + str(max_decisions))
        if len(tsav)>0:
            self.tsav = tsav
        else:
            self.tsav = np.arange(max_decisions)
        print("self.tsav " + str(self.tsav))

        self.env = env
        self.pol = pol
        self.nbRepetitions = nbRepetitions
        self.horizon = horizon
        self.nbArms = env.nbArms
        self.nbPulls = np.zeros((self.nbRepetitions, self.nbArms))
        self.cumReward = np.zeros((self.nbRepetitions, len(self.tsav)))
        self.env.restart()
        self.choices = np.zeros((self.nbRepetitions, max_decisions))
        self.rewards = np.zeros((self.nbRepetitions, max_decisions))
        self.means = np.zeros((self.nbRepetitions, self.nbArms))
                 
        # progress = ProgressBar()
        min_events = float('+inf')
        for k in range(nbRepetitions): # progress(range(nbRepetitions)):
            if nbRepetitions < 10 or k % (nbRepetitions/10)==0:
                print k
            result = env.play(pol, horizon, max_decisions)
            self.nbPulls[k, :] = result.getNbPulls()
            self.cumReward[k, :] = np.cumsum(result.rewards)[self.tsav]
            self.choices[k, :] = result.choices
            self.rewards[k, :] = result.rewards
            print("mean rew: " + str(self.cumReward[k, 1000]/1000))

            choice_rewards = np.zeros(self.nbArms)
            choice_frequencies =  np.zeros(self.nbArms)
            for choice, reward in zip(result.choices,result.rewards):
                choice_rewards[int(choice)] += reward
                choice_frequencies[int(choice)] += 1

            self.means[k, :] = np.divide(choice_rewards, choice_frequencies)

            if result.nbEvents < min_events:
                min_events = result.nbEvents

        self.tsav = np.arange(min_events)
        # progress.finish()
     
    def meanReward(self):
        return sum(self.cumReward[:,-1])/len(self.cumReward[:,-1])

    def meanNbDraws(self):
        return np.mean(self.nbPulls ,0) 

    def meanRegret(self):
        #return (1+self.tsav)*np.mean(self.bestExpect) - np.mean(self.cumReward, 0)
        return (1+self.tsav)*max([arm.expectation for arm in self.env.arms]) - np.mean(self.cumReward, 0)[self.tsav]

    def regret(self):
        print("and now tsav " + str(self.tsav))
        print(((1+self.tsav)*max([arm.expectation for arm in self.env.arms]))[-1])
        return (1+self.tsav)*max([arm.expectation for arm in self.env.arms]) - self.cumReward[:, self.tsav]




