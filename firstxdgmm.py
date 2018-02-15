import sklearn
import nose
import astroML_addons
import astroML
import scipy
import pandas
import xdgmm
from astropy.io import fits
import csv
import os
from shutil import copyfile
import numpy as np

import requests
import ast

def fetchFirstVals():
	
	deltaW = []
	sigW = []
	w1 = []
	w2 = []
	w1s = []
	w2s = []
	mjd = []

	directorystr = './csvfiles/notNull/'
	directory = os.fsencode(directorystr)
	filelist = os.listdir(directory)
	for file in filelist:
		filestr = os.fsdecode(file)
		if(filestr.endswith(".csv")):
			readfile = open('./csvfiles/notNull/'+filestr, 'r')
			reader = csv.reader(readfile)
			for i, row in enumerate(reader):
				if i == 1:
					w1.append(row[0])
				if i == 2:
					w1s.append(row[0])
				if i == 3:
					w2.append(row[0])
				if i == 4:
					w2s.append(row[0])

	deltaW = [float(x) - float(y) for x in w1 for y in w2]
	sigW = [np.sqrt(float(x)**2 + float(y)**2) for x in w1s for y in w2s]
#	print(deltaW)
#	print(sigW)
	return deltaW, sigW

		
deltaW, sigW = fetchFirstVals()

xdgmm = XDGMM()

param_range = np.array([1, 2])

bic, optimal_n_comp, lowest_bic = xdgmm.bic_test(X, Xerr, param_range)

