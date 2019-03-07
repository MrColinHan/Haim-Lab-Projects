#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 17:23:47 2019

@author: Han
"""
from re import compile
'''
    This script removes Accession groups in a Nucleotide sequence fasta file based 
    on the Accession numbers I found in the AA Sequence. Since special characters('#''$''?''X') only appear
    in AA Sequence which is converted from a Nucleotide sequence, i can only find them in 
    AA sequence first then remove the same accession numbers in a nucleotide sequence
    
    INPUTS: 
            lefroverDir: directory of the Accession numbers (output of the "Find_accession_inAAsequence(inFasta).py" )
            NucleotideDir: directory of the nucleotide sequence fasta file
            outputDir: directory of the output file
            outputName: directory of the output file
'''

# Inputs ###############################################################################################
leftoverDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/3.5.19 kr(rm 61 access nums)/for raid/AccessionNumbers(with# & $).txt"
NucleotideDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/3.5.19 kr(rm 61 access nums)/for raid/HCV E1 and E2 USA 1a AA frame 1.fas"
outputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/3.5.19 kr(rm 61 access nums)/for raid/"
outputName = "HCVNucleotide(without#$).fas"
########################################################################################################

ACCESSION_MATCHER = compile(r'[A-Za-z]{2}\d{6}$|[A-Za-z]\d{5}$|[A-Za-z]{2}\_\d{6}$')


fasContent = [] # a list for all nucleotide sequence 
TXTContent = [] # a list for all accession numbers that contain special characters
outputList = [] # a list used to save clean sequence


def readFasta(x,y):  # read a fasta file x and store into a list y
    file = open(x,"r")
    for line in file:
        y.append(line)


readFasta(NucleotideDir,fasContent)  # read the nucleotide sequence into fasContent list


def getAccessNum(string):
    """
    extract accession from the given string, returns the first match if there are multiple matches
    :param string: the string to extract accession from
    :return: the extracted accession
    """
    #print(string)
    return ACCESSION_MATCHER.findall(string)[0]


def readTXT():  # read a text file into a list
    file = open(leftoverDir,'r+')
    rows = file.readlines()
    for i in rows:
        TXTContent.append(i[:-1])


readTXT()

print("TXT file: ")
print('There are '+ str(len(TXTContent))+ ' accession numbers need to be removed.')
print("\n")
print("Fasta File: ")

HeaderList = [] # a list contains index of all headers starting with ">"


def getHeaderIndex (x,y):  # read x save to y
    i = 0
    while i < len(x):
        if x[i][0] == '>':
            y.append(i)
        i += 1


getHeaderIndex(fasContent,HeaderList)
print("before removing, input fasta has: "+ str(len(HeaderList)) + " samples.")


def remove():  # Remove the accession numbers and then write the remaining into a new fasta file
    
    i = 0
    output= open(outputDir+outputName,"w+") 
    while i < (len(HeaderList)-1):
        fragment = fasContent[(HeaderList[i]+1):HeaderList[i+1]]
        #print(fragment)
        if getAccessNum(fasContent[HeaderList[i]]) not in TXTContent:
            output.write(fasContent[HeaderList[i]])
            for j in (fragment):
                output.write(j)
        i += 1
    if getAccessNum(fasContent[HeaderList[-1]]) not in TXTContent:
        for p in fasContent[HeaderList[-1]:]:
            output.write(p)
    output.close


remove()

outputFasContent = [] # a list for all sequence of output nucleotide fasta file
readFasta(outputDir+outputName,outputFasContent) # read the output fasta file into a list  
outputHeaderList = []
getHeaderIndex (outputFasContent,outputHeaderList)
print("after removing, output fasta has " + str(len(outputHeaderList))+ " samples.")
print("since: "+ str(len(TXTContent))+ "+" +str(len(outputHeaderList))+" = "+ str(len(TXTContent)+len(outputHeaderList)))
if (len(TXTContent)+len(outputHeaderList)) == len(HeaderList):
    print("so it's correct")
else:
    print("so this is not correct! Something is wrong! ")

# debug: 

inputAccessList = []
for i in HeaderList:
    inputAccessList.append(getAccessNum(fasContent[i]))
outputAccessList = []
for i in outputHeaderList:
    outputAccessList.append(getAccessNum(outputFasContent[i]))
outputAccessList = outputAccessList + TXTContent

print('\n')
print('Debug:')
print(len(inputAccessList))
print(len(outputAccessList))


def debug():
    i = 0
    while i < len(inputAccessList):
        if inputAccessList[i] in inputAccessList[i+1:]:
            print(inputAccessList[i])
        i += 1
            
    '''count = 0
    for i in outputAccessList:
        if i in inputAccessList:
            count += 1
    print(count)'''


debug()



