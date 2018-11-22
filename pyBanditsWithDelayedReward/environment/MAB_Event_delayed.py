# -*- coding: utf-8 -*-
'''General simulation routine based in time events'''

__author__ = "Miguel Martin, Antonio Jimenez, Alfonso Mateos"
__version__ = "1.0"

from Result import *
from Environment import Environment
from collections import deque
from policy.BlackBox import BlackBox
from Queue import PriorityQueue
import numpy as np
import random as rn
import time
from sets import Set

class MABEventDelayed(Environment):
    """Multi-armed bandit problem with arms given in the 'arms' list"""
    
    def __init__(self, arms, conf, rndProcess):
        self.rndProcess = rndProcess
        self.arms = arms
        self.nbArms = len(arms)
        self.conf = conf
        self.last_arm_index = 0
        self.events = PriorityQueue()
        self.policy = None
        self.black_box = False
        self.delay_decisions = dict()
        self.all_delays = []
        self.choice_delays = []
        self.update_delays = []
         #To remove
        self.track_arms = Set([0,1,2,3,4,5,6,7,8,9])


        # supposed to have a property nbArms

    def arm_event(self,t, horizon, sim_index):
        init_time = time.time()
        choice = self.policy.choice()
        #To remove
        if choice in self.track_arms:
            self.track_arms.remove(choice)
         #To remove
        if not self.track_arms:
            print("todos en iteration: " + str(sim_index))
            self.track_arms.add(10)

        elapsed_time = (time.time() - init_time)
        self.choice_delays += [elapsed_time]
        t_rew = self.arms[choice].draw()
        reward, r = self.conf.getDelayedReward(t_rew, t)
        delay = r + t
        #print "reward: " + str(reward)
        #print "delay reward: " + str(delay)

        self.events.put((delay, 'r', reward, choice, t, sim_index))

        t_next = self.rndProcess.draw(t/3600)

        #print "next decision: " + str(t + t_next)
        if (t + t_next) < horizon:
            self.events.put((t + t_next, 'a', 0, 0, t, sim_index))
            for (key, value) in self.delay_decisions.items():
                self.delay_decisions[key] = value + 1

            self.delay_decisions[sim_index] = 0


    def play(self, reference_policy, horizon, max_decisions):

        self.policy = reference_policy

        self.policy.startGame()

        result = Result(self.nbArms, max_decisions)

        sim_index = 0
        random_init_time = rn.uniform(0, 24)

        first_event = self.rndProcess.draw(random_init_time)
        self.arm_event(first_event, horizon, sim_index)

        while not self.events.empty():
            event_time, event_type, reward, arm, t, idx = self.events.get()
            #print "event dequeue: " + str(event_time)

            if event_type == 'r':
                init_time = time.time()
                self.policy.getReward(int(arm), reward)
                update_time = (time.time() - init_time)
                self.update_delays +=[update_time]
                if idx < max_decisions:
                    result.store(idx, int(arm), reward)

                    delay = self.delay_decisions.pop(idx, 'None')
                    if delay is not 'None':
                        self.all_delays += [delay]

            else:
                self.arm_event(event_time, horizon, sim_index)
                sim_index += 1


        print len(self.all_delays)
        print "mean delays " + str(np.mean(self.all_delays))
        # print("choice delays: " + str(np.sum(self.choice_delays[:50000])) + " " +
        #       str(self.choice_delays[10]) + " " +
        #       str(self.choice_delays[1000]) + " " +
        #       str(self.choice_delays[50000]))
        #
        # print("update delays: " + str(np.sum(self.update_delays[:50000])) + " " +
        #       str(self.update_delays[10]) + " " +
        #       str(self.update_delays[1000]) + " " +
        #       str(self.update_delays[50000]))
        #
        # print("total_time " + str(np.sum(self.choice_delays[:50000]) + np.sum(self.update_delays[:50000])))

        return result

    def restart(self):
        for i in self.arms:
            i.restart()
        self.conf.restart()
        self.events = PriorityQueue()

