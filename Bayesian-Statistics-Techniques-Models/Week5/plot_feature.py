import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import pymc3 as pm

from scipy.special import expit

def plot_feature(data,feature,ax,bins=50):
    xmin = data[feature].min()
    xmax = data[feature].max()
    ax.hist(data[data['visit']==0][feature],bins=bins,range=(xmin,xmax),histtype='step',label='visit=0',density=1.)
    ax.hist(data[data['visit']==1][feature],bins=bins,range=(xmin,xmax),histtype='step',label='visit=1',density=1.)
    ax.set_xlabel(feature)
    ax.legend(loc='best')

data = pd.read_csv('criteo-uplift-v2.1.csv',nrows=5e5)
fig,ax = plt.subplots(4,3,figsize=(16,12))
fig.tight_layout()
n = 11
for i in range(n):
    ix = i % 3
    iy = i // 3
    plot_feature(data,'f'+str(i),ax[iy,ix])
fig.savefig('feature.png')

