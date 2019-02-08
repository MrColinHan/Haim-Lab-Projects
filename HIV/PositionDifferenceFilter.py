#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 16:54:47 2019

@author: Han
"""

'''
    This script compare the same position's percentage between two clades. 
    If the difference is less than a cutoff percent, then change both percentage
    to 0. 

'''

import csv 

# Inputs ================================================================================================

Bdir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.6.19 new Euclidean/B_distribution.csv"
Cdir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.6.19 new Euclidean/C_distribution.csv"
AEdir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.6.19 new Euclidean/AE_distribution.csv"
OutputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.6.19 new Euclidean/"
B_OutputName = "B_filtered.csv"
C_OutputName = "C_filtered.csv"
AE_OutputName = "AE_filtered.csv"
cutoff = 1 

# ========================================================================================================


B = []
C = []
AE = []

def readCSV(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row) 
        
readCSV(Bdir,B)
readCSV(Cdir,C)
readCSV(AEdir,AE)

testB = B[:3]
testC = C[:3]

def difference(x,y):
    i = 1
    while i < len(x):
        a = 0
        while a<21:
            if ((abs(float(x[i][a])) - abs(float(y[i][a]))) < cutoff):
                x[i][a] = 0
                y[i][a] = 0
            a += 1
        i += 1
difference(testB,testC)


def writeCsv(x,y):
    with open(OutputDir+y,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()
            
writeCsv(B,B_OutputName)
writeCsv(C,C_OutputName)
writeCsv(AE,AE_OutputName)










