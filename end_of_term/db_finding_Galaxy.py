"""
Maclean Rouble and Soud Kharusi
WISE Querying Algorithm through coadd and multiepoch data

--This programme searches through SDSS DR8,  catalogue of galaxies,
and pulls their RA and DEC.
--Then it searches through the coadd WISE data,
and checks how many measurements with SNR>3 for w1 and w2 for that object.
--If there are measurements with SNR>3,
 we take the objects ID and search for it in the multiepoch photometry
table to pull light curves (w1,w1sigma, w2,w2sigma) and create csv files
--We are using w1mpro_ep not w1flux_ep, this holds for w2-4 as well.
"""

from astropy.io import fits
import csv
import os
import requests
import ast

def makeCSV(filename_input, source_id_input, ra_input, dec_input, mjd_input, w1_input, w1sig_input, w2_input, w2sig_input, w3_input, w3sig_input, w4_input, w4sig_input):
    outfile = open('../csvfiles_galaxies/'+filename_input+'.csv', 'w') #creates/opens the csv file for appending
    wr = csv.writer(outfile)

    wr.writerow(["source_id (source_id_mf): ", source_id_input])
    wr.writerow(["RA: ", ra_input])
    wr.writerow(["DEC: ", dec_input])
    wr.writerow(" ")

    wr.writerows([["mjd: "], mjd_input])
    wr.writerows([["W1: "], w1_input])
    wr.writerows([["W1sigma: "], w1sig_input])
    wr.writerows([["W2: "], w2_input])
    wr.writerows([["W2sigma: "], w2sig_input])
    wr.writerows([["W3: "], w3_input])
    wr.writerows([["W3sigma: "], w3sig_input])
    wr.writerows([["W4: "], w4_input])
    wr.writerows([["W4sigma: "], w4sig_input])
    #wr.writerows([["moon_masked: "], moon_masked_input])

    print("CSV file written for object (RA_DEC): " + filename_input)

#Searches coadd catalog (All Wise Source catalog), pulls #measurements of w1,w2 with SNR>3.
#Then if nonzero, takes source_id and does another search for source_id_mf in the multiepoch Table
#Outputs csv files for light curves.
def WISE(req, RA, DEC):
    url_coadd = 'https://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-query?spatial=cone&radius=10&catalog=allwise_p3as_psd&selcols=ra,dec,source_id,w1nm,w2nm&objstr=' + RA + '+' + DEC + '&outfmt=1'

    ret_coadd = requests.get(url_coadd).text

    #TEST: printing the full results from url query
    #print("ASCII Result File:" +"\n"+ ret_coadd)

    #Split the text into lines
    retLines_coadd = ret_coadd.split("\n")

    #TEST: printing the line with all the data
    #print("Data line:" + "\n" + retLines_coadd[-2])

    #Split line of interest into compenents
    retData_coadd = retLines_coadd[-2].split()

    if(retData_coadd[5]=='8004'):
        print("Error 1034: 08004. ORACLE not available ORA-27101: shared memory realm does not exist Solaris-AMD64")
        return

    #With these selcols, source_id, w1nm and w2nm are columns 4, 5 and 6 respectively.
    ra = retData_coadd[0]
    dec = retData_coadd[1]
    source_id = retData_coadd[4]
    w1nm = retData_coadd[5]
    w2nm = retData_coadd[6]

    #TEST: Print w1nm, w2nm. These should be integers.
    #print("w1nm:", w1nm)
    #print("w2nm:", w2nm)

    if((w1nm == '0') or (w2nm == '0') or w1nm == 'null' or w2nm == 'null'):
            print("---SKIP: FOUND NO w1 or w2 values for object (RA_DEC): " +" "+req)
            return

    #Searching by id
    url_mep = "https://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-query?spatial=none&catalog=allwise_p3as_mep&selcols=source_id_mf,ra,dec,mjd,w1mpro_ep,w1sigmpro_ep,w2mpro_ep,w2sigmpro_ep,w3mpro_ep,w3sigmpro_ep,w4mpro_ep,w4sigmpro_ep,moon_masked&constraints=source_id_mf=" + "'" + source_id + "'" + "&outfmt=1" #searching by source_id_mf
    #Searching by RA and DEC
    #url_mep = "https://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-query?spatial=cone&radius=10&catalog=allwise_p3as_mep&selcols=source_id_mf,ra,dec,mjd,w1mpro_ep,w1sigmpro_ep,w2mpro_ep,w2sigmpro_ep,w3mpro_ep,w3sigmpro_ep,w4mpro_ep,w4sigmpro_ep,moon_masked&objstr=" + RA + "+" + DEC + "&outfmt=1"
    ret_mep = requests.get(url_mep).text

    #TEST: printing the full results from url query
    #print("ASCII Result File:" +"\n"+ ret_mep)

    #Split text into lines
    retLines_mep = ret_mep.split("\n")

    firstDataLine = 47 #depends on selcols, check by printing full ASCII file.

    #TEST: printing the first line with all the data, starts on line 47 for mep with these selcols.
    #print("First line of data:" + "\n" + retLines_mep[firstDataLine])

    mjd = []
    w1 = []
    w1sig = []
    w2 = []
    w2sig = []
    w3 = []
    w3sig = []
    w4 = []
    w4sig = []
    #moon_masked=[]

    for i in range(firstDataLine, len(retLines_mep)-1):
        retData_mep = retLines_mep[i].split()

        #TEST: See if the lines are being split correctly and going to last data line.
        #print(retData_mep)

        mjd.append(retData_mep[5])
        w1.append(retData_mep[6])
        w1sig.append(retData_mep[7])
        w2.append(retData_mep[8])
        w2sig.append(retData_mep[9])
        w3.append(retData_mep[10])
        w3sig.append(retData_mep[11])
        w4.append(retData_mep[12])
        w4sig.append(retData_mep[13])
        #moon_masked.append(retData_mep[14])

    #def makeCSV(filename_input, source_id_input, ra_input, dec_input, w1_input, w1sig_input, w2_input, w2sig_input, w3_input, w3sig_input, w4sig_input, w4sig_input, moon_masked_input)
    makeCSV(req, source_id, ra, dec, mjd, w1, w1sig, w2, w2sig, w3, w3sig, w4, w4sig)

def main(): #raiding galaxy the catalogue, acts as the main.
    cat = fits.open("../../Catalogs/galSpecInfo-dr8.fits") #Change this line to match your file system.
    #TEST: How many objects in the database
    #print("There are: ", len(cat[1].data['RA']), " objects in the database") #based on the number of RA values

    #Starting Number for searching entries. Starts on previous multiple of 10.
    try:
        file = open('EntryNumber_Gal.txt', 'r')
        text = file.read()
        EntryStart = text.split()[3]
        file.close()
    except FileNotFoundError:
        print("File not found, starting from zero.")
        EntryStart = 0


    for entry in range(int(EntryStart), len(cat[1].data['RA'])): #change these range values to say which ones to download
    #Problems start around object 42
        RA = cat[1].data['RA'][entry]
        DEC = cat[1].data['DEC'][entry]
        #print(cat[1].data.names) #prints all searchable fields in DR14, OBJ_ID and THING_ID are a thing!? Wut.

        #Text file to tell us what entry we got to.
        if(entry%10==0):
            f = open('EntryNumber_Gal.txt','w')
            f.write("Last entry written: "+str(entry))
            f.close()
        print("Entry:", entry)

        #Let's go.
        RA_DEC_str = "" + str(RA) + "_" + str(DEC) #this is just parsing the RA and DEC
        WISE(RA_DEC_str, str(RA), str(DEC)) #Running WISE

main()
