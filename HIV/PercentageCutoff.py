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

Bdir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.6.19 new Euclidean/B(no15,16,17,310,311).csv"
Cdir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.6.19 new Euclidean/C(no15,16,17,310,311).csv"
AEdir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.6.19 new Euclidean/AE_distribution.csv"
OutputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.6.19 new Euclidean/"
B_OutputName = "(BvsAE)B_cutoffed.csv"
C_OutputName = "(CvsAE)C_cutoffed.csv"
AE_OutputName = "(CvsAE)AE_cutoffed.csv"
cutoff = 1 
'''ALSO NEED TO CHANGE THE ARGUMENTS IN FUNCTIONS AT THE END'''
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

testB = [["x"],[1,0.1,0,0,0,0,6,0,3,0,0,0,0,0,98,  0,0,0,0,0,0,0]]
testC = [["x"],[2,0,  5,0,0,0,7,0,4,0,0,0,0,0,98.5,0,0,0,0,0,0,0]]

def difference(x,y):
    i = 1
    while i < len(x):
        
        a = 1
        while a<len(x[i]):
            if ((abs(float(x[i][a]) - float(y[i][a]))) < cutoff): 

                x[i][a] = 0
                y[i][a] = 0
                
                
            a += 1
        i += 1
    return

'''=====================CHANGE ARGUMENTS HERE========================================'''
#difference(B,C)
#difference(B,AE)
difference(AE,C)
'''============================================================='''

def writeCsv(x,y):
    with open(OutputDir+y,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()

'''=====================CHANGE ARGUMENTS HERE========================================'''
#writeCsv(B,B_OutputName)
writeCsv(C,C_OutputName)
writeCsv(AE,AE_OutputName)
'''============================================================='''










