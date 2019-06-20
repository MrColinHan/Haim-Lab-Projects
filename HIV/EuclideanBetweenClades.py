#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 15:31:33 2019

@author: Han
"""
# Inputs ================================================================================================
inputFile = r"/Users/Han/Documents/Haim_Lab(2018_summer)/6.20.19_fig4B_centroids/6.20.19_fig4B_logconverted_rm0.6.csv"

# ========================================================================================================



# NON-PNGS points
_137AE = []
_289A1 = []
_295C = []
_332AE = []
_339AE = []
_398C = []


# PNGS-Centroids
_137cen = []
_289cen = []
_295cen = []
_332cen = []
_339cen = []
_398cen = []

# Euclidean fomular
def Euclidean(list1,list2):
    squareSum = 0
    for i in range(len(list1)):
        squareSum = squareSum + ((float(list2[i]) - float(list1[i]))**2)    
    return (math.sqrt(squareSum))

# calculate distance between 137AE and 6 centroids
#                            289A1 and 6 centroids
#                            295C ...
#                            ......

csvList = []

def readCSV(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row) 
        
readCSV(inputFile,csvList)

#for i in csvList[1:]:
    #print(i[0]+i[1])

_137AE = list(map(float,csvList[1][2:]))
_289A1 = list(map(float,csvList[3][2:]))
_295C = list(map(float,csvList[5][2:]))
_332AE = list(map(float,csvList[7][2:]))
_339AE = list(map(float,csvList[9][2:]))
_398C = list(map(float,csvList[11][2:]))
non_PNGS = {'137AE':_137AE,'289A1':_289A1,'295C':_295C,'332AE':_332AE,'339AE':_339AE,'398C':_398C}

_137cen = list(map(float,csvList[2][2:]))
_289cen = list(map(float,csvList[4][2:]))
_295cen = list(map(float,csvList[6][2:]))
_332cen = list(map(float,csvList[8][2:]))
_339cen = list(map(float,csvList[10][2:]))
_398cen = list(map(float,csvList[12][2:]))
centroids = {'137cen':_137cen,'289cen':_289cen,'295cen':_295cen,'332cen':_332cen,'339cen':_339cen,'398cen':_398cen}

#for i in non_PNGS:
    #print(non_PNGS[i][1])

#for i in centroids:
    #print(centroids[i][1])

for n_Z in non_PNGS:
    print("")
    for cen in centroids:
        print(n_Z + " vs " + cen + " : " + str(Euclidean(non_PNGS[n_Z],centroids[cen]))) 


