import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import pymc3 as pm

from scipy.special import expit

input_path = 'output/btreat-b0-b4_1e4-1e4/trace.p'

trace = pickle.load(open(input_path,'rb'))
print(sum(trace['btreat']>0.)/len(trace['btreat']))
