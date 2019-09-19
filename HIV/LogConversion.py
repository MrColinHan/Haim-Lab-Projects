#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 15:16:07 2019

@author: Han
"""

'''
    This script automate the process of log conversion for the percentages of
    AA distribution. 
    step1 : define a threshold, if percentage <= threshold, then = 0
    step2 : if percentage == 0, then = 0.1 (or 0.01,...)
    step3 : log(percentage)+1 (if step2 was 0.01 then should +2)
    
'''

import csv 
import math


# Inputs ================================================================================================

inputdir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/8.21.19_4pos_dist/8.21.19_need_log(vs_B).csv"
OutputDir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/8.21.19_4pos_dist/"
OutputName = "8.21.19_(vs_B)log_converted_0.75.csv"
changeZeroTo = 0.1  # can be 0.1, or 0.001
threshold = 0.75 # if <= threshold%, then change to 0
zStartsAt = 2 # Z starts at first row's index 4 (note: index starts at 0)

InputContainsProperties = False  # True : if input format is [Position][Z]...
clade = "C"                      # False: if input format is [Clade][Region][Position][Year][Z]...
year = "[2007,2015]"


# ========================================================================================================
add = None         
if changeZeroTo == 0.1:  # if changed 0 to 0.1, then add 1. If changed to 0.01, then add 2
    add = 1
if changeZeroTo == 0.01:
    add = 2


csvList = []

def readCSV(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row) 
        
readCSV(inputdir,csvList)

debugList = csvList[:] # preserve an original csv list for debugging

def addProperties():  # add three properties so that the output can be used in Euclidean.py
    csvList[0].insert(0,"Clade")
    csvList[0].insert(2,"Year")
    csvList[0][1] = "Position"
    for i in csvList[1:]:
        i.insert(0,clade)
        i.insert(2,year)
        
if InputContainsProperties == True:
    addProperties()

def logConversion():
    i = 1
    while i < len(csvList):
        j = zStartsAt           # Z starts at first row's index 
        while j < len(csvList[i]):
            if float(csvList[i][j]) <= threshold:
                csvList[i][j] = 0
            print(csvList[i][j])
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
#print(csvList)
