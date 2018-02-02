import sklearn
import nose
import astroML_addons
import astroML
import scipy
import pandas
import xdgmm
from astropy.io import fits

import requests
import ast

def WISE(req, RA, DEC): #M: tbh I'm not sure what 'req' does?

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
            #print(retCutData)
            mjd.append(retCutData[9])
            w1.append(retCutData[10])
            w1sig.append(retCutData[11])
            w2.append(retCutData[13])
            w2sig.append(retCutData[14])

    print(mjd) #modified julian date
    print(w1)
    print(w1sig)
    print(w2)
    print(w2sig)

    #for x in range(0, len(ret)):
    #    print("\n", ret[x])

def dr14(): #raiding the quasar catalogue
    cat = fits.open("DR14Q_v3_1.fits")
    #for entry in len(cat[1].data['RA']): #get them all
    for entry in range(20):
        RA = cat[1].data['RA'][entry]
        DEC = cat[1].data['DEC'][entry]
        RA_DEC_str = "" + str(RA) + " " + str(DEC) #this is just parsing it
        WISE(RA_DEC_str, str(RA), str(DEC)) 


#WISE('294.1256623 -22.4012492')
dr14()


#wget command through cis module in python to run terminal commands to get data / query wget

#next:
##feed xdgmm
###average each object's mjd, w1, w1sig, w2, w2sig?
###
