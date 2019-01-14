#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 15:05:31 2019

@author: Han
"""

import os
import csv 


leftoverDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.14/leftover (question mark and X).csv"
NucleotideDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.14/2016-2017 USA H3N2 nucleotide.fasta"
#NucleotideDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.14/codeTest.fasta"


outputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.14/"
outputName = "Nucleotide (no X or question mark).fas"



fasContent = []
csvContent = []

def readFasta(x,y):
    file = open(x,"r")
    for line in file:
        y.append(line)
        
readFasta(NucleotideDir,fasContent)

def readCSV():
    file = open(leftoverDir)
    reader = csv.reader(file)
    for row in reader:
        csvContent.append(row)   

readCSV()


def NumRowsEachAccession():
    rowCounts = 1
    if fasContent[0][0] == '>':  
        
        for i in fasContent[1:]:
            if i[0] != '>':
                rowCounts = rowCounts+1
            else:
                return (rowCounts)
    else:
        print("this file doesnt start with '>'")

NumRowsPerAccessionNum = NumRowsEachAccession()
print("Each Accession number has "+ str(NumRowsPerAccessionNum)+ " rows")


AccessFasList = []
def AccessInFas(x):
    i = 0
    while i < len(x):
        AccessFasList.append(x[i][1:9])
        i = i + NumRowsPerAccessionNum

AccessInFas(fasContent)
print("before removing, fasta has " + str(len(AccessFasList))+ " samples.")

AccessCSVList = []
def AccessInCSV():
    for i in csvContent[1:]:
        AccessCSVList.append(i[0])

AccessInCSV()
print("leftover CSV has "+str(len(AccessCSVList)))




def remove():
    i = 0
    output= open(outputDir+outputName,"w+") 
    while i < len(fasContent):
        if fasContent[i][1:9] in AccessCSVList:
            i = i+30
        else:
            output.write(fasContent[i])
            i = i+1

    output.close

remove()

# check the length of fasta file contents again 


outputFasContent = []
readFasta(outputDir+outputName,outputFasContent)


AccessFasList = []
AccessInFas(outputFasContent)
print("after removing, fasta has " + str(len(AccessFasList))+ " samples.")











