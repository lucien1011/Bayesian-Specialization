import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import pymc3 as pm

from scipy.special import expit

data = pd.read_csv('criteo-uplift-v2.1.csv',nrows=1e5)

coords = {"observation": data.index.values}
with pm.Model(coords=coords) as regression_model:
    # data
    treat = pm.Data('treatment', data['treatment'], dims='observation')
    x0 = pm.Data("x0", data["f0"], dims="observation")
    x6 = pm.Data("x6", data["f6"], dims="observation")
    
    # priors
    a = pm.Normal("a", mu=0, sigma=1)
    btreat = pm.Normal('btreat', mu=0, sigma=1e2)
    b0 = pm.Normal("b0", mu=0, sigma=1)
    b6 = pm.Normal("b6", mu=0, sigma=1e2)
    
    # linear model
    μ = a + b0 * x0 + b6 * x6 + btreat * treat
    #μ = b0 * x0 + b6 * x6 + btreat * treat
    
    # likelihood
    pm.Bernoulli("y", logit_p=μ, observed=data["visit"], dims="observation")

with regression_model:
    step = pm.Metropolis(vars=[a,btreat,b0,b6])
    trace = pm.sample(int(1e4), tune=int(1e4),step=step)

pickle.dump(trace,open('trace.p','wb'))

