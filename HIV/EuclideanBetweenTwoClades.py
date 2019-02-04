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

# Inputs ###############################################################################################

Bdir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.1.19 HIV Euclidean(B,C,AE)/2.1.19 Clade_B_FullPos_LogConverted.csv"
Cdir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.1.19 HIV Euclidean(B,C,AE)/2.1.19 Clade_C_FullPos_LogConverted.csv"
AEdir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.1.19 HIV Euclidean(B,C,AE)/2.1.19 Clade_AE_FullPos_LogConverted.csv"
OutputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/2.1.19 HIV Euclidean(B,C,AE)/"
OutputName = "C_AE_Distance.csv"
'''Also need to change the arguments in main()'''

########################################################################################################



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

BCdistance = main(C,AE) #########################################################

def writeCsv(distancelist):
    with open(OutputDir+OutputName,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(distancelist)
    file.close()
            
writeCsv(BCdistance)







