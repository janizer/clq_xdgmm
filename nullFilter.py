#checks previously-created csv files and selects only those which have no null values

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

import requests
import ast

def checkNull(arr):
	val = 0
	for i in range(len(arr)):
		if arr[i] == 'null':
			val = val + 1
	return val

def readCSV():
	
	directorystr = './csvfiles/'
	directory = os.fsencode(directorystr)
	filelist = os.listdir(directory)
	for file in filelist:

		val = 0
		filestr = os.fsdecode(file) #omfg python3
		if(filestr.endswith(".csv")):
			readfile = open('./csvfiles/'+filestr, 'r')
			reader = csv.reader(readfile)	
			for row in reader:
				if checkNull(row) != 0: #we found a null value
					val = val +1
			if val == 0:
				print('File ' + filestr + ' is not null.')
				copyfile('./csvfiles/'+filestr, './csvfiles/notNull/'+filestr)


readCSV()