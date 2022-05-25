import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import pymc3 as pm

from scipy.special import expit

trace = pickle.load(open('trace.p','rb'))
print(trace)

var_names = ['a','btreat','b0','b6']

print(az.ess(trace,var_names=var_names))

plt.figure()
az.plot_trace(trace,var_names=var_names)
plt.savefig("trace.png")
plt.clf()

plt.figure()
az.plot_autocorr(trace,var_names=var_names)
plt.savefig("autocorr.png")
plt.clf()

plt.figure()
az.plot_posterior(
    trace,
    group="posterior",
    var_names=var_names,
    hdi_prob="hide",
    kind='hist',
    bins=40,
)
plt.savefig("posterior.png")
plt.clf()
