#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 15:12:13 2019

@author: Han
"""
'''NEED TO UPDATE: cannot check 'X' if the accession number contains 'X' '''
''' 
    For FLU project
    This script finds all Accession numers that contain 'X' or '?' in a AA Sequence fasta file. 
    
    INPUTS: 
            AADir: the directory  AA sequence
            outputDir: directory for the ourput file
            outputName: the name for the output file. 
    
'''


# Inputs ================================================================================================
AADir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.23.19(12-15flu)/B-14-15 AA Sequence(with X).fas"
outputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.23.19(12-15flu)/"
outputName = "C-14-15 AccessionNumbers(withX).txt"
# =======================================================================================================

from re import compile
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
    print(count) # print the amount of accession numbers that are stored
    
findX() # execute the function 
print(AccessionList) # print all the accession numbers that contains 'X' or '?'
print(len(AccessionList)) # print the length of AccessionList to double check the number


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
checkDup()
           


'''
leftoverDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.14/leftover (question mark and X).csv"
csvContent = []
def readCSV():
    file = open(leftoverDir)
    reader = csv.reader(file)
    for row in reader:
        csvContent.append(row)   

readCSV()
AccessCSVList = [] #################
def AccessInCSV():
    for i in csvContent[1:]:
        AccessCSVList.append(i[0])
AccessInCSV()
print(AccessCSVList)
print(len(AccessCSVList))

def debug():
    for i in AccessCSVList:
        if i not in AccessionList:
            print(i)

print("debug: ")
debug()

def special(x):
    count = 0
    for i in AAContent:
        count += 1
        if x in i:
            print(count-1)         
'''





