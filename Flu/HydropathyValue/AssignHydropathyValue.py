#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 17:09:00 2019

@author: Han
"""

# This script does two tasks:
# 1. assigns each amino acid a hydropathy value 
# 2. remove rows with "x" or "?" to a new tab 

'''This script is merged into the Volatility.py.'''


###################################################################

import csv 

inputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.3/PNGS Grouped AA sequence.csv"
OutputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.8/"
OutputName = "output.csv"
input = open(inputDir)


fileContent = []
def readFile():
    reader = csv.reader(input)
    for row in reader:
        fileContent.append(row)

readFile()
title = fileContent[0]

leftover = []
def filter():
    leftover.append(fileContent[0])
    leftoverPosition = []
    for i in fileContent:
        positions = []
        for j in i:
            if j == "?" or j == "X":
                positions.append(title[i.index(j)])
                leftoverAccess = []
                for k in leftover:
                    leftoverAccess.append(k[0])
                if i[0] not in leftoverAccess:
                    leftover.append(i)
                    
        if len(positions) != 0:
            leftoverPosition.append(positions)

    print("AA Positions for each row's 'X' or '?' : "+ "\r\n" + "\r\n" + str(leftoverPosition))
    output = open(OutputDir+"leftover (question mark and X).csv","w")
    writer = csv.writer(output)
    writer.writerows(leftover)
    output.close

filter()

HYDROPATHY_SCORE_TABLE = {
    'A': 0.68,
    'C': 0.733,
    'D': 0.19,
    'E': 0.203,
    'F': 1,
    'G': 0.584,
    'H': 0.304,
    'I': 0.958,
    'K': 0.403,
    'L': 0.953,
    'M': 0.782,
    'N': 0.363,
    'P': 0.759,
    'Q': 0.376,
    'R': 0.167,
    'S': 0.466,
    'T': 0.542,
    'V': 0.854,
    'W': 0.898,
    'Y': 0.900,
    'Z': 0,
    '-': 1.5
}
            
def AssignHydropathy():
    del leftover[0]
    #del fileContent[0]
    for i in leftover:
        fileContent.remove(i)
    for j in fileContent:
        for k in j:
            if k in list(HYDROPATHY_SCORE_TABLE.keys()):
                
                fileContent[fileContent.index(j)][j.index(k)] = HYDROPATHY_SCORE_TABLE[k]
    
    
    
    
    '''for j in fileContent:
        for k in j:
            if k == "M":
                fileContent[filecontent.index(j)][j.index(k)] = 0.782'''

    #fileContent.insert(0,title)
    output = open(OutputDir+OutputName,"w")
    writer = csv.writer(output)
    writer.writerows(fileContent)
    output.close

AssignHydropathy()