#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 15:05:31 2019

@author: Han
"""



#input##########################
leftoverDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.16.19/2640AccessionWithXandQuestionMark.txt"
NucleotideDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.16.19/2016-2017 USA H3N2 nucleotide(2640 samples).fasta"
#output##########################
outputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.16.19/"
outputName = "2640Nucleotide (without XandQuestionMark).fas"



fasContent = []
TXTContent = []

def readFasta(x,y):
    file = open(x,"r")
    for line in file:
        y.append(line)
        
readFasta(NucleotideDir,fasContent)
print("TXT file (accession numbers with ? or X): ")
def readTXT():
    file = open(leftoverDir,'r+')
    rows = file.readlines()
    for i in rows:
        TXTContent.append(i[0:8])
    file.close()

readTXT()
print(TXTContent)
print('There are '+ str(len(TXTContent))+ ' accession numbers need to be removed.')

print("\n")
print("Fasta File: ")
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
print("Each Accession number has "+ str(NumRowsPerAccessionNum)+ " rows(for debugging)")


AccessFasList = []
def AccessInFas(x):
    i = 0
    while i < len(x):
        AccessFasList.append(x[i][1:9])
        i = i + NumRowsPerAccessionNum

AccessInFas(fasContent)
print("before removing, input fasta has " + str(len(AccessFasList))+ " samples.")
'''
AccessCSVList = []
def AccessInCSV():
    for i in csvContent[1:]:
        AccessCSVList.append(i[0])

AccessInCSV()
print("leftover CSV has "+str(len(AccessCSVList)))



'''
def remove():
    i = 0
    output= open(outputDir+outputName,"w+") 
    while i < len(fasContent):
        if fasContent[i][1:9] in TXTContent:
            i = i+NumRowsPerAccessionNum
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
print("after removing, output fasta has " + str(len(AccessFasList))+ " samples.")









