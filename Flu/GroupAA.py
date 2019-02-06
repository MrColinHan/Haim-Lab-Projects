#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:04:00 2019

@author: Han
"""

'''
    This script takes grouped Accession numbers and match them with their AA
    in PNGS AA csv file. 
'''
import ast
import csv

# Inputs ================================================================================================

txtDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.29.19 Ans Pos(BCAE)/Flu_grouped_AA/17-18Groups.txt"
PNGSDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.29.19 Ans Pos(BCAE)/Flu_grouped_AA/I-17-18 PNGS AA CSV(without X).csv"
OutputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.29.19 Ans Pos(BCAE)/Flu_grouped_AA/"
OutputName = "17-18GroupedAA.csv"

#========================================================================================================


def readTXT(): # read a text file into a list
    file = open(txtDir,'r+')
    return (file.read())
    file.close()

NumList = ast.literal_eval(readTXT())

group2 = NumList[1] 

csvContent = []
def readCSV():
    file = open(PNGSDir)
    reader = csv.reader(file)
    for row in reader:
        csvContent.append(row)   

readCSV()
#row2 = csvContent[1]

emptyList = []
GroupedAAList = []
def match():
    
    for group in NumList:
        for i in group:
            for j in csvContent:
                if i == j[0]:
                    GroupedAAList.append(j)
                    print( i + "  " + str(csvContent.index(j)+1))
        GroupedAAList.append(emptyList)
        
match()


GroupedAAList.insert(0,csvContent[0])
def writeCsv():
    with open(OutputDir+OutputName,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(GroupedAAList)
    file.close()
            
writeCsv()
            
            
            
            
            
            
            