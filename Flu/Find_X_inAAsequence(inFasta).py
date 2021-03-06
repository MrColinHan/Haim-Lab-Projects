#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 15:12:13 2019

@author: Han
"""

''' 
    For FLU project
    This script finds all Accession numers that contain 'X' or '?' in a AA Sequence fasta file. 
    
    INPUTS: 
            AADir: the directory  AA sequence
            outputDir: directory for the ourput file
            outputName: the name for the output file. 
    
'''


# Inputs ================================================================================================
AADir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/9.6.19_flu/B_aa.fas"
outputDir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/9.6.19_flu/"
outputName = "C_AA_AccessionNumbers(withX).txt"
# =======================================================================================================

from re import compile
# use regular expre define accession_num format: for now I've only seen AB123456 and A12345
ACCESSION_MATCHER = compile(r'[A-Za-z]{2}\d{6}|[A-Za-z]\d{5}')

AAContent = [] # a list for all AA sequence

def readFasta(x,y):  # read the AA Sequence fasta file and then store them in list AAContent
    file = open(x,"r")
    for line in file:
        y.append(line)

readFasta(AADir,AAContent) # execute the function

def getAccessNum(string):
    """
    extract accession from the given string, returns the first match if there are multiple matches
    :param string: the string to extract accession from
    :return: the extracted accession
    """
    #print(string)
    return ACCESSION_MATCHER.findall(string)[0]


AccessionList = [] # a list for all Accession Numbers that contains 'X' or '?'
def findX(): # find 'X' or '?' in the AA sequence and then store the accession number in a list
    count = 0
    i = 1
    while (i < len(AAContent)):
        if ('?' in AAContent[i]) or ('X' in AAContent[i]):# check 'X' and '?'
            count = count + 1
            if (getAccessNum(AAContent[i-1]) not in AccessionList):# make sure there's no duplicate in the list
                AccessionList.append(getAccessNum(AAContent[i-1])) # if not in list, add to list
        i += 2
    print(f"{count} accession num found: ") # print the amount of accession numbers that are stored
    
findX() # execute the function
print(AccessionList) # print all the accession numbers that contains 'X' or '?'
print(f"\ndouble check amount: {len(AccessionList)} \n") # print the length of AccessionList to double check the number


def writeTxt(): # write the AccessionList into a new text file 
    output= open(outputDir+outputName,"w+") 
    for i in AccessionList:
        output.write(i+"\n") # one number one line 
    output.close
writeTxt() # execute the function 

def checkDup(): # check the duplicate again in the AccessionList
    i = 0
    while (i<len(AccessionList)):
        for j in AccessionList[i+1:]:
            if AccessionList[i] == j:
                print("find duplicate")  # if there is a duplicate, print it 
                print(j)
        i = i+1
checkDup() # execute the function 






