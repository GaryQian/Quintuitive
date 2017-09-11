import csv
import cPickle as pickle
import numpy as np

filename = 'prices9-11-2017'

prices = dict()
with open(filename + '.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	ticker = ""
	data = list()
	for row in reader:
		if (ticker != row['ticker']):
			prices[ticker] = data
			print ticker
			ticker = row['ticker']
			data = list()
		try:
			data.append(float(row['close']))
		except:
			print("Could not add " + row['close'])
	prices[ticker] = data
	

print 'Dumping data...'
output = open(filename + '.dat', 'wb')
pickle.dump(prices, output)
print 'Done!'