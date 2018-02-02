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

import requests
import ast

def WISE(req, RA, DEC): 

    #req.replace(' ','+')
    url = 'https://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-query?spatial=cone&catalog=allwise_p3as_mep&objstr=' + RA + '+' + DEC + '&size=5&outfmt=1'
    #can use &selcols= to narrow down returns
    #url = uri+req
    ret = requests.get(url).text
    #scrape = '['+ret.split('cacheResponse([[')[1].split(',[')[0].split(',',1)[1]
    #data = ast.literal_eval(scrape)
    #print(data)
    #print(ret)

    # File output into txt for tests
    #f = open('testOut.txt','w')
    #f.write(ret)
    #f.close()

    #Split into lines and get rid of all headers, data starts at line 72
    retCutLines = ret.split("\n")[72:]
    #print(retCutLines)
    mjd = []
    w1 = []
    w1sig = []
    w2 = []
    w2sig = []
    for x in range(0, len(retCutLines)-1):
            retCutData = retCutLines[x].split()
            mjd.append(retCutData[9])
            w1.append(retCutData[10])
            w1sig.append(retCutData[11])
            w2.append(retCutData[13])
            w2sig.append(retCutData[14])

    if(checkNull(w1) == 0) or (checkNull(w2) == 0): #there were no w1 or w2 values for this object
        return

    #print(mjd) #modified julian date
    makeCSV(mjd, w1, w1sig, w2, w2sig, req)
    #print(w1)
    #makeCSV(w1, req)
    #print(w1sig)
    #makeCSV(w1sig, req)
    #print(w2)
    #makeCSV(w2, req)
    #print(w2sig)
    #makeCSV(w2sig, req)

    #for x in range(0, len(ret)):
    #    print("\n", ret[x])

def dr14(): #raiding the quasar catalogue
    cat = fits.open("../DR14Q_v3_1.fits")
    #for entry in len(cat[1].data['RA'])/100.0: #get them all
    for entry in range(2000, 5000):
        RA = cat[1].data['RA'][entry]
        DEC = cat[1].data['DEC'][entry]
        print(entry)

        RA_DEC_str = "" + str(RA) + "_" + str(DEC) #this is just parsing it
        WISE(RA_DEC_str, str(RA), str(DEC)) 

def makeCSV(data1, data2, data3, data4, data5, obj):
    outfile = open('./csvfiles/'+obj+'.csv', 'w') #creates/opens the csv file for appending
    wr = csv.writer(outfile)
    wr.writerow(data1)
    wr.writerow(data2)
    wr.writerow(data3)
    wr.writerow(data4)
    wr.writerow(data5)
    print("done file for obj " + obj)

def checkNull(arr):
    val = 0
    for i in range(len(arr)):
        if arr[i] != 'null':
            val = val + 1 #keep track of how many non-zero entries we find
    return val


#WISE('294.1256623 -22.4012492')
dr14()

