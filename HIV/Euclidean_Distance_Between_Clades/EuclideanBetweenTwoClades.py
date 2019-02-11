#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 10:25:29 2019

@author: Han
"""

'''
    This script takes log converted AA distribution of multiple clades as input and then 
    calculate the 21 factor Euclidean Distance of each position between any combination of two clades
'''

import csv
import math

# Inputs ================================================================================================
#CSV input format needs to be | Clade | Position | Year | Z | N | ......
Bdir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.6.19 new Euclidean/(BvsAE_cutoff1)B_Log.csv"
Cdir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.6.19 new Euclidean/(CvsAE_cutoff1)C_Log.csv"
AEdir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.6.19 new Euclidean/(CvsAE_cutoff1)AE_Log.csv"
OutputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.6.19 new Euclidean/"
OutputName = "(cutoff1)C_AE_Distance.csv"

'''ALSO NEED TO CHANGE THE ARGUMENTS IN main()'''

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


def Euclidean(list1,list2):
    squareSum = 0
    for i in range(len(list1)):
        squareSum = squareSum + ((float(list2[i]) - float(list1[i]))**2)    
    return (math.sqrt(squareSum))
'''
i  = [2,2,2,2,2]
j = [2,2,2,2,2]
w = B[1][3:]
q = C[1][3:]
print(Euclidean(w,q))'''

def main(clade1,clade2):
    result = []
    positions = []
    distances = []
    i = 1
    while i < len(clade1):
        positions.append(clade1[i][1])
        distances.append(Euclidean(clade1[i][3:],clade2[i][3:]))
        i += 1
    result.append(positions)
    result.append(distances)
    return result
# ========================================================================================================
'''CHANGE THE ARGUMENTS HERE'''
BCdistance = main(C,AE) 
# ========================================================================================================


def writeCsv(distancelist):
    with open(OutputDir+OutputName,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(distancelist)
    file.close()
            
writeCsv(BCdistance)







