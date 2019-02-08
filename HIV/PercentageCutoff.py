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

testB = [["x"],[1,0.1,0,0,0,0,6,0,3,0,0,0,0,0,98,  0,0,0,0,0,0,0]]
testC = [["x"],[2,0,  5,0,0,0,7,0,4,0,0,0,0,0,98.5,0,0,0,0,0,0,0]]

def difference(x,y):
    i = 1
    while i < len(x):
        
        a = 1
        while a<len(x[i]):
            if ((abs(float(x[i][a]) - float(y[i][a]))) < cutoff): 
                '''CONSIDER! IF BOTH PERCENTAGE ARE (100,100) OR (99,99.5), THE IT GOES TO 0???'''
                '''SHOULD WE CHECK THAT THE PERCENTAGE SHOULD BE OVER SOME VALUE FIRST THEN CHECK THE CUROFF'''
                '''OR , ONLY WHEN ONE percentage is 0 and the other is less than 1'''
                x[i][a] = 0
                y[i][a] = 0
                
                
            a += 1
        i += 1
    return
difference(B,C)
#difference(B,AE)
#difference(AE,C)


def writeCsv(x,y):
    with open(OutputDir+y,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


writeCsv(B,B_OutputName)
writeCsv(C,C_OutputName)
#writeCsv(AE,AE_OutputName)











