#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 15:16:07 2019

@author: Han
"""

'''
    This script automate the process of log conversion for the percentages of
    AA distribution. 
    step1 : if percentage == 0, then = 0.1 (or 0.01,...)
    step2 : log(percentage)+1 (if last step was 0.01 then should +2)
    
'''

import csv 
import math


# Inputs ================================================================================================

inputdir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.18.19 distribution/164167CSV.csv"
OutputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.18.19 distribution/"
OutputName = "2.18.19 MDSInput.csv"
clade = "C"   
changeZeroTo = 0.1  # can be 0.1, or 0.001
add = 1             # if changed 0 to 0.1, then add 1. If changed to 0.01, then add 2
year = "[2007,2015]"
'''
addProperties is for input data who only has Position property column
If the the input data format is [Clade][Position][Year][Z]...
Then comment out addProperties part
'''
# ========================================================================================================

csvList = []

def readCSV(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row) 
        
readCSV(inputdir,csvList)

debugList = csvList[:] # preserve an original csv list for debugging
'''
def addProperties():  # add three properties so that the output can be used in Euclidean.py
    csvList[0].insert(0,"Clade")
    csvList[0].insert(2,"Year")
    csvList[0][1] = "Position"
    for i in csvList[1:]:
        i.insert(0,clade)
        i.insert(2,year)

addProperties()
'''
def logConversion():
    i = 1
    while i < len(csvList):
        j = 3
        while j < len(csvList[i]):
            if float(csvList[i][j]) == 0:
                csvList[i][j] = changeZeroTo
                csvList[i][j] = math.log10(csvList[i][j])+add
            else:
                csvList[i][j] = math.log10(float(csvList[i][j]))+add
            j += 1
        i += 1
logConversion()


def writeCsv(x):
    with open(OutputDir+OutputName,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()
            
writeCsv(csvList)
