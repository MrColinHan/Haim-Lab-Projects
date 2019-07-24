#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 03:55:09 2019

@author: Han
"""

import csv
# Inputs ================================================================================================
inputFile = r"/Users/Han/Documents/Haim_Lab(2018_summer)/7.23.19_fig4_centroids/22pos/CSV/AS_CSV.csv"
outdir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/7.23.19_fig4_centroids/22pos/CSV/separated/"
clade = "BAS" # BNA, BEU, BKR, BAS
# ========================================================================================================


def readCSV(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row) 
   

def writeCsv(x,y,z): # x is input list, y is OutputDir, z is OutputName
    with open(y+z,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()   
    
csvList = []
readCSV(inputFile,csvList)  # read input into list






#writeCsv(test_out, outdir, out_file_name)

pos = ""  # save position name
out_w = None  # save output file
out_file_name = None # constract output file name


i = 0
count = 0
while i < len(csvList):
    
    try:
        int(csvList[i][0]) # if true: then zip(i , i+1)
        pos = csvList[i][0] # get position name
        out_file_name = clade + "_ALL_" + pos + ".csv"  # construct output file name
        out_w = list(map(list, zip(csvList[i][1:], csvList[i+1][1:]))) # save output content
        writeCsv(out_w, outdir, out_file_name)
        count += 1
        print(f"{out_file_name} generated")
        
        i += 1
    except:  
        i += 1
        continue 
print(f"{count} files generated total")

    
"""
testout = []
readCSV(outdir+"BNA_ALL_208.csv",testout)
print(testout)
"""