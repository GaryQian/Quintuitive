
import cPickle as pickle
import numpy as np
import math

def error(targ, other):
	if len(targ) != len(other):
		return math.inf
	return np.sum(np.absolute(targ - other)) / len(targ)
	

#targ = target stock we want to predict
#src = dataset we want to correlate with
#amt = number of results to return
def correlate(targ, src, amt):
	minError = math.inf
	
	return 0;

filename = 'prices9-11-2017'

#Dict with key as ticker and val as closing price as a float
data = pickle.load(open(filename + ".dat", "rb"))

