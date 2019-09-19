#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 03:55:09 2019

@author: Han
"""

import csv
# Inputs ================================================================================================
inputFile = r"/Users/Han/Documents/Haim_Lab(2018_summer)/7.24.19_new_MDS/p_value_input/164_167_need_separate.csv"
outdir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/7.24.19_new_MDS/p_value_input/164_167_separated/"
zStartsAt = 2 # Z starts at first row's index 4 (note: index starts at 0)
pos_at = 1
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
region = "" # save region name
clade = "" # sace clade name
out_w = None  # save output file
out_file_name = None # constract output file name


i = 0
count = 0
while i < len(csvList):
    
    try:
        int(csvList[i][pos_at]) # if true: then zip(i , i+1)
        pos = csvList[i][pos_at] # get position name
        clade = csvList[i][0]
        region = csvList[i+1][0]
        out_file_name = clade + f"_{region}_" + pos + ".csv"  # construct output file name
        out_w = list(map(list, zip(csvList[i][zStartsAt:], csvList[i+1][zStartsAt:]))) # save output content
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