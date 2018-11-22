# -*- coding: utf-8 -*-
'''Simulation of online reward updated architectures'''

__author__ = "Miguel Martin, Antonio Jimenez, Alfonso Mateos"
__version__ = "1.0"


from environment.MAB_Event_delayed import MABEventDelayed
from environment.Delayed_Conf_Random_poisson import Delayed_Conf_Random_poisson
from environment.Delayed_dependent_reward_Conf_Random_poisson import Delayed_DR_Conf_Random_poisson
from arm.Bernoulli import Bernoulli
from arm.Bernoulli_Delay import Bernoulli_Delay
from policy.UCB import UCB
from numpy import *
from policy.DMED import DMED
from policy.klUCB import klUCB
from policy.klUCBplus import klUCBplus
from policy.PossibilisticReward import PossibilisticReward
from policy.PossibilisticReward_chernoff2 import PossibilisticReward_chernoff2
from policy.PossibilisticReward_Bern1 import PossibilisticReward_Bern1
from policy.besa import besa
from Evaluation import *
from kullback import *
from policy.BlackBox import BlackBox
from environment.NH_Poisson_Proccess import NHPoissonProcess
from environment.NH_Poisson_Proccess import generate_ratio_function
import sys


scenarios = ['bernoulli_low_var_random', 'bernoulli_high_var_random', 'bernoulli_low_var_random_DR', 'bernoulli_high_var_random_DR']


scenario = scenarios[int(sys.argv[1])]

nbRep = int(sys.argv[3])
horizon = int(sys.argv[4])

print 'nbRep :' + str(nbRep)
print 'horizon :' + str(horizon)
print 'scenario: ' + scenario

max_decisions = 500000


def get_policy(nbArms, trunc_value, index):
    original_policies = [DMED(nbArms, trunc_value), klUCBplus(nbArms, trunc_value),
                         besa(nbArms, trunc_value),
                         UCB(nbArms, trunc_value),
                         klUCB(nbArms, trunc_value),
                         PossibilisticReward(nbArms, trunc_value, scale=1),
                         PossibilisticReward_chernoff2(nbArms, trunc_value, scale=1),
                         PossibilisticReward_Bern1(nbArms, trunc_value, confidence=0.1)
                         ]

    black_box_policies = [BlackBox(nbArms, pol) for pol in original_policies]
    policy_list = original_policies + black_box_policies

    if index == 'all':
        return policy_list
    else:
        return [policy_list[int(index)]]


def execute_simulation(nbRep, horizon, pol_index, process, tr):
    if scenario == 'bernoulli_low_var_random':
        config = Delayed_Conf_Random_poisson(1./80, 300)
        env = MABEventDelayed(
            [Bernoulli(p, samples=nbRep * horizon) for p in [0.1, 0.05, 0.05, 0.05, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01]],
            config, process)
        trunc_value = 1.0

    elif scenario == 'bernoulli_high_var_random':
        config = Delayed_Conf_Random_poisson(1./80, 300)
        env = MABEventDelayed(
            [Bernoulli(p, samples=nbRep * horizon) for p in [0.5, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45]],
            config, process)
        trunc_value = 1.0

    elif scenario == 'bernoulli_low_var_random_DR':
        config = Delayed_DR_Conf_Random_poisson(1./150, 480)
        env = MABEventDelayed(
            [Bernoulli_Delay(p, 1./150) for p in [0.1, 0.05, 0.05, 0.05, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01]],
            config, process)
        trunc_value = 1.0

    else:
        config = Delayed_DR_Conf_Random_poisson(1./150, 480)
        env = MABEventDelayed(
            [Bernoulli_Delay(p, 1./150) for p in [0.5, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45]],
            config, process)
        trunc_value = 1.0

    policies = get_policy(env.nbArms, trunc_value, pol_index)
    print 'policiy: ' + str(policies)

    #tsav = int_(linspace(100, horizon - 1, 200))

    for wrap_pol in policies:
        ev = Evaluation(env, wrap_pol, nbRep, max_decisions, horizon)
        print ev.meanReward()
        print ev.meanNbDraws()
        meanRegret = ev.meanRegret()
        regret = ev.regret()
        cumReward = ev.cumReward
        prefix = ''
        nbPulls = ev.nbPulls
        means = ev.means

        if wrap_pol.__class__.__name__ == 'BlackBox':
            policy = wrap_pol.policy
            prefix = 'BlackBox_'
        else:
            policy = wrap_pol

        name_klucb = str(getattr(policy, "klucb", "none"))
        name_scale = str(getattr(policy, "scale", "none"))
        name_gap = str(getattr(policy, "gap", "none"))
        name_conf = str(getattr(policy, "confidence", "none"))
        base_name = "data_delayed/" + scenario + "/" + prefix + policy.__class__.__name__ + "_" + str(
            nbRep) \
                    + "-" + str(horizon) + "_" + name_klucb + "_" + name_scale + "_" + name_gap + "_" + name_conf
        save(base_name + "_" + tr + "_" + "regret", regret)
        save(base_name + "_" + tr + "_" + "nbPulls", nbPulls)
        save(base_name + "_" + tr + "_" + "means", means)


params_low = [(0, 0.005),
              (8, 0.005),
              (10, 0.006),
              (12, 0.008),
              (13, 0.008),
              (15, 0.006),
              (17, 0.006),
              (19, 0.01),
              (20, 0.01),
              (21, 0.009)]

params_high = [(0, 0.005),
               (8, 0.025),
               (10, 0.075),
               (12, 0.55),
               (13, 0.55),
               (15, 0.2),
               (17, 0.2),
               (19, 0.65),
               (20, 0.65),
               (21, 0.55)]


params_very_high = [(0,0.2),
                    (8,0.4),
                    (10,2),
                    (12,7),
                    (13,7),
                    (15,3.2),
                    (17,3.2),
                    (19,9.5),
                    (20,9.5),
                    (21, 7.)]


traffic = str(sys.argv[5])
if traffic == 'high_traffic':
    params = params_high

elif traffic == 'very_high_traffic':
    params = params_very_high

else:
    params = params_low


f = generate_ratio_function(params)
pr = NHPoissonProcess(f)

execute_simulation(nbRep, horizon, str(sys.argv[2]), pr, traffic)

exit(0)
