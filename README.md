# clq_xdgmm 
last update: 07/05/2018
contact: maclean.rouble@mail.mcgill.ca & soud.alkharusi@mail.mcgill.ca

HELLO AND WELCOME!

This is a summary of our work during Winter 2018 in the Haggard group at McGill. 

The folder you just opened contains the following: xdgmm_modelGenerator.ipnb, object_flagging.ipnb, file_digging.ipynb, db_finding.py, and db_finding_galaxy.py all written in Python 3 (including xdgmm which was written in 2.7 originally)

The xdgmm_modelGenerator file is used to build the models. It opens csv files, reads the data and spits out the component Gaussians.The file is broken up into separate sections that can be run separately (true for all iPython Notebook files), some of these, take a while to run.  

object_flagging looks through all the csv files you feed into it and flags the ones that have abnormal W1-W2 values. 

file_digging does a some analysis on the flagged objects (or whatever you feed into it). For example, it finds CLQ candidates by vary more than X amount. It also tries to spot which ones stay in the varied state for a while. 

db_finding_quasar and db_finding_galaxy looks through the SDSS DR14 catalog and cross-references categorized objects (quasars or galaxies respectively) with ones in the WISE data. If the object is also in the WISE catalog is then pulls the light curves of that object from WISE multiepoch photometry tables. You can read up on how the URL works on the WISE/IPAC website. The code outputs csv files to a location of your choice. It also will start on a previous multiple of 10 if it crashes. 

The xdgmm_modelGenerartor code is based off of that found in https://github.com/tholoien/XDGMM which is also useful to look through. 
