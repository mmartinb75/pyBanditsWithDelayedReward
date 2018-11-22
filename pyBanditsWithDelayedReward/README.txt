        pyBandits simiulation in delayed reward enviroment
        It has been developed extending the pyBandits python code of  Olivier Capp�, Aur�lien Garivier, Emilie Kaufmann.
     ............................................................

     python classes of Olivier Capp�, Aur�lien Garivier, Emilie Kaufmann.:

            Evaluation.py		  Class for running a bandit experiment
            kullback.py			  Module with Kullback-Leibler utilities
            Result.py			  Class for summarizing a bandit experiments

            arm/
                arm/__init__.py
                arm/Arm.py		  Generic arm class
                arm/Bernoulli.py		  Class for common arm distributions (possibly
                arm/Exponential.py	    truncated)
                arm/Gaussian.py
                arm/Poisson.py

            C/
                C/kullback.c		  C-coded version of the Kullback-Leibler
                C/Makefile		    utility module (will supersede kullback.py
                C/README.txt		    if installed)
                C/setup.py

            environment/
                environment/__init__.py
                environment/Environment.py  Generic environment class
                environment/MAB.py	  Multi-armed bandit class (note that a MAB is
    				    a collection of arms and can thus use
    				    arms with differents types)

            policy/
                policy/__init__.py
                policy/Policy.py		  Generic policy classes
                policy/IndexPolicy.py
                policy/BayesUCB.py	  Class for policies, names should be explicit
                policy/KLempUCB.py	    (note that klUCB can use the different
                policy/klUCB.py		    forms of KL divergences defined in
                policy/Thompson.py	    kullback, in particular, UCB is a special
                policy/UCB.py                 case of klUCB)
                policy/UCBV.py

            posterior/
                posterior/__init__.py
                posterior/Posterior.py	  Generic class for posteriors
                posterior/Beta.py		  Posteriors in Bernoulli/Beta experiments


     New python classes created by  Miguel Martín, Antonio Jiménez and Alfonso Mateos:


            dictionaries.py
            generateBatchResults_eventMode.py
            generateBatchResults_eventMode_with_seed.py
            generateRandomResults_eventMode.py
            generateRandomResults_eventMode_with_seed.py


            arm/
                arm/Bernoulli_Delay.py


            environment/
                environment/Delayed_dependent_reward_Conf_batch_poisson.py
                environment/Delayed_Conf_batch_poisson.py
                environment/Delayed_Conf_Random_poisson.py
                environment/Delayed_dependent_reward_Conf_Random_poisson.py
                environment/MAB_Event_delayed.py
                environment/NH_Poisson_Proccess.py

            policy/
                policy/besa.py
                policy/BlackBox.py
                policy/PossibilisticReward.py
                policy/PossibilisticReward_Bern1.py
                policy/PossibilisticReward_chernoff2.py

-----------------------------------------------------------
To execute different simulations write on of these:

For batch architecture simulations:

python -u   generateBatchResults_eventMode.py scenarios method nbRep horizon traffic
python -u   generateBatchResults_eventMode_with_seed.py scenarios method nbRep horizon traffic seed

where:
    scenarios is one of ['bernoulli_low_var_batch', 'bernoulli_high_var_batch', 'bernoulli_low_var_batch_DR', 'bernoulli_high_var_batch_DR']
    method [0 - 9] where:
        0 - DMED
        1 - klUCBplus
        2 - besa
        3 - UCB
        4 - klUCB
        5 - PossibilisticReward(nbArms, trunc_value, scale=1),
        6 - PossibilisticReward_chernoff2(nbArms, trunc_value, scale=1),
        7 - PossibilisticReward_Bern1(nbArms, trunc_value, confidence=0.1)
        8 - blackbox over DMED
        9 - blackbox over klUCBplus
        10 - blackbox over besa
        11 - blackbox over UCB
        12 - blackbox over klUCB
        13 - blackbox over PossibilisticReward(nbArms, trunc_value, scale=1),
        14 - blackbox over PossibilisticReward_chernoff2(nbArms, trunc_value, scale=1),
        15 - blackbox over PossibilisticReward_Bern1(nbArms, trunc_value, confidence=0.1)
    nbRep is the num of simulations to get averages
    horizon is the horizon or num repetitions of MAB problem
    traffic is one of ['high_traffic', 'low_traffic']
    seed is the seed for simulated with a specific start seed.


The result is stored in three numpy file for posterior visualization and summarization:
    regrets - a numpy array of dim(nbRep, horizon) that store the cumulative regret for each simulation in each time step
    means - a numpy array of dim(nbRep, num of arms) that store the final sample mean of every arm in every simulation
    nbPulls - a numpy array of dim(nbRep, num of arms) that store the number of times each arm has been pulled in each simulation




For online architecture simulations:
python -u   generateRandomResults_eventMode.py scenarios method nbRep horizon traffic
python -u   generateRandomResults_eventMode_with_seed.py scenarios method nbRep horizon traffic seed


where:
    scenarios is one of ['bernoulli_low_var_batch', 'bernoulli_high_var_batch', 'bernoulli_low_var_batch_DR', 'bernoulli_high_var_batch_DR']
    method [0 - 9] where:
        0 - DMED
        1 - klUCBplus
        2 - besa
        3 - UCB
        4 - klUCB
        5 - PossibilisticReward(nbArms, trunc_value, scale=1),
        6 - PossibilisticReward_chernoff2(nbArms, trunc_value, scale=1),
        7 - PossibilisticReward_Bern1(nbArms, trunc_value, confidence=0.1)
        8 - blackbox over DMED
        9 - blackbox over klUCBplus
        10 - blackbox over besa
        11 - blackbox over UCB
        12 - blackbox over klUCB
        13 - blackbox over PossibilisticReward(nbArms, trunc_value, scale=1),
        14 - blackbox over PossibilisticReward_chernoff2(nbArms, trunc_value, scale=1),
        15 - blackbox over PossibilisticReward_Bern1(nbArms, trunc_value, confidence=0.1)
    nbRep is the num of simulations to get averages
    horizon is the horizon or num repetitions of MAB problem
    traffic is one of ['very_high_traffic', 'high_traffic', 'low_traffic']
    seed is the seed for simulated with a specific start seed.


The result is stored in three numpy file for posterior visualization and summarization:
    regrets - a numpy array of dim(nbRep, horizon) that store the cumulative regret for each simulation in each time step
    means - a numpy array of dim(nbRep, num of arms) that store the final sample mean of every arm in every simulation
    nbPulls - a numpy array of dim(nbRep, num of arms) that store the number of times each arm has been pulled in each simulation



------------------------------

From Olivier Capp�, Aur�lien Garivier, Emilie Kaufmann. README file:


These files have been tested under python2.6. The C extension requires a C
compiler and installed python header files; it is not required to run the
code: it just speeds up some critical computations (and is recommended for
running policy/KLempUCB).


# HOWTO:

To compile the C functions (which is optional), use "cd C; make".

To run the demo, simply type: "python demo.py". By editing the file, you will
be able to run alternative demos easily, and the way to run other experiments
should be quite straightforward.


# NOTES:

By default, most policies (policy/UCB, policy/KLempUCB, policy/klUCB when used
with the default choice for parameter klucb) require the rewards to be bounded
in [0,1], but other bounds can be used thanks to the parameters 'amplitude'
and 'lower': the rewards must then be no smaller than 'lower' and no larger
than 'lower+amplitude'.

Warning: arguments 'lower' and 'amplitude' should not be modified when
policy/klUCB is used with a distribution-specific divergence 'klucb', even for
bounded rewards. For instance, when policy/klUCB(klucb=klucbPoisson) is used
with 'arm/Poisson(2, 10)', the parameter 'amplitude' should not be set to 10
in policy/klUCB(klucb=klucbPoisson) because that would cause the rewards to be
inadequately divided by 10, see the scenario 1 in 'demo.py'.


    --
    $Id: README.txt,v 1.7 2012-07-05 17:03:40 cappe Exp $
