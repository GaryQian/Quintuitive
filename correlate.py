
import cPickle as pickle
import numpy as np
import math
import heapq
import copy
import matplotlib.pyplot as plt
from multiprocessing import Pool

inf = 999999999
threads = 7

def error(targ, other, type = 'linear', norm = True):
	#Convert to numpy and normalize
	if (norm):
		targ = normalize(targ)
		other = normalize(other)
	if len(targ) != len(other):
		return inf
	if (type == 'square'):
		return (np.sum(np.absolute(targ - other)) / len(targ)) ** 2
	#Linear error by default
	return np.sum(np.absolute(targ - other)) / len(targ)
	
def normalize(arr):
	arr = np.array(arr)
	return arr / np.max(arr)

#targ = target stock we want to predict
#other = dataset we want to correlate with
#amt = number of results to return
#detail = the resolution of comparison, higher = finer comarisons
def correlate(targ, other, amt, detail, norm = True):
	storage = dict()
	h = []
	h.append(0)
	storage[0] = 0

	if (norm):
		targ = np.array(targ)
		other = np.array(other)
	length = len(targ)
	for scale in range(1, detail + 2):
		for i in range(0, int((len(other) - scale) - length*scale), scale):
			arr = other[i:i+length*scale+scale:scale]
			err = error(targ, arr[0:len(arr)-1], 'square', norm)
			if (err < 1-h[0]):
				heapq.heappush(h, 1-err)
				storage[1-err] = copy.copy(arr)
				if (len(h) > amt):
					junk = heapq.heappop(h)
					if junk in storage:
						del storage[junk]
	#Build output
	out = []
	h = h[::-1]
	h.sort()
	i = 0
	for err in h:
		i += 1
		if (i > amt):
			break
		if err != 0:
			if (err in storage):
				out.append((1-err, storage[err]))
	return out;

filename = 'prices9-11-2017'

#Dict with key as ticker and val as closing price as a float
data = pickle.load(open(filename + ".dat", "rb"))

predictTicker = 'AAPL'
otherTickers = data.keys()[:800]
print otherTickers
interval = 20
days = 10
skip = 50
start = 1000
accuracy = 0
total = 0
avoidedLoss = 0;
other = [0]
for ticker in otherTickers:
	if len(data[ticker][:]) > 0:
		other = np.concatenate((other, normalize(data[ticker][:])))
	print len(other)
for i in range(0,len(data[predictTicker]) - interval - start,skip):
	if (i % 5 == 0):
		print "Status:" + str(i)
	if (i >= skip * days):
		break
	targ = normalize(data[predictTicker][i + start:i + start + interval + 1])
	result = correlate(targ[:len(targ)-1], other, 3, 3, False)
	plt.plot(range(interval + 1), targ, 'r--', range(interval + 1), result[0][1], 'b--')
	plt.show()
	break
	predict = 0
	for n in range(len(result)):
		arr = result[n][1]
		predict += arr[len(arr) - 1] - arr[len(arr) - 2]
	predict /= len(result)
	actual = targ[len(targ) - 1] - targ[len(targ) - 2]
	
	#inverted because ???
	if (predict > 0):
		accuracy += actual
	else:
		avoidedLoss += actual
		
	'''if (np.sign(predict) == np.sign(actual)):
		accuracy += 1
	total += 1'''
print accuracy
#float(accuracy) / float(total)
		
	
	





