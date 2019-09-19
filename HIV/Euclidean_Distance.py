#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 13:24:59 2019

@author: Han
"""

import math 
import csv
# Inputs ================================================================================================
inputFile = r"/Users/Han/Documents/Haim_Lab(2018_summer)/8.12.19/calcu_dist_input.csv"
OutputDir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/8.12.19/"
OutputName = "dist_outputs.csv"
# ========================================================================================================


# Euclidean fomular
def Euclidean(list1,list2):
    squareSum = 0
    for i in range(len(list1)):
        squareSum = squareSum + ((float(list2[i]) - float(list1[i]))**2)    
    return (math.sqrt(squareSum))


csvList = []


def readCSV(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row) 
    
    
readCSV(inputFile,csvList)


def writeCsv(x):
    with open(OutputDir+OutputName,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()
            
Output_list = []

_169_CEN  = csvList[1][2:]
_181_CEN = csvList[2][2:]
_346_CEN = csvList[3][2:]


_169_samples = []
_181_samples = []
_346_samples = []

for i in csvList:
    if i[0] == ('169' or 169):
        _169_samples.append(i)
    if i[0] == ('181' or 181):
        _181_samples.append(i)
    if i[0] == ('346' or 346):
        _346_samples.append(i)
        
        
Output_list.append([f"Porition_169 contains {len(_169_samples)} samples"])
Output_list.append([f"Porition_181 contains {len(_181_samples)} samples"])
Output_list.append([f"Porition_346 contains {len(_346_samples)} samples"])
Output_list.append(["================================================="])
Output_list.append(["Distances between centroids: "])
Output_list.append(["169cen vs 181cen: " + str(Euclidean(_169_CEN,_181_CEN ))])
Output_list.append(["169cen vs 346cen: " + str(Euclidean(_346_CEN,_169_CEN ))])
Output_list.append(["181cen vs 346cen: " + str(Euclidean(_346_CEN,_181_CEN ))])
Output_list.append(["================================================="])
Output_list.append([f"Distances between 169_cen and its {len(_169_samples)} samples: "])

_169_dists = []
_169_names = []
for i in _169_samples:
    _169_names.append(i[1])
    _169_dists.append(Euclidean(_169_CEN,i[2:]))
    
print(len(_169_dists))
Output_list.append(_169_names)
Output_list.append(_169_dists)

Output_list.append(["================================================="])
Output_list.append([f"Distances between 181_cen and its {len(_181_samples)} samples: "])

_181_dists = []
_181_names = []
for i in _181_samples:
    _181_names.append(i[1])
    _181_dists.append(Euclidean(_181_CEN,i[2:]))
    
print(len(_181_dists))
Output_list.append(_181_names)
Output_list.append(_181_dists)

Output_list.append(["================================================="])
Output_list.append([f"Distances between 346_cen and its {len(_346_samples)} samples: "])

_346_dists = []
_346_names = []
for i in _346_samples:
    _346_names.append(i[1])
    _346_dists.append(Euclidean(_346_CEN,i[2:]))
print(len(_346_dists))
Output_list.append(_346_names)
Output_list.append(_346_dists)





writeCsv(Output_list)










