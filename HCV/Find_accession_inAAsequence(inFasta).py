#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 23:38:36 2019

@author: Han
"""
from re import compile
''' 
    FOR HCV project
    This script finds all Accession numbers that contain special characters in a AA Sequence fasta file. 
    
    INPUTS: 
            AADir: the directory  AA sequence
            outputDir: directory for the ourput file
            outputName: the name for the output file. 
    !!!: 1. Three possible forms of accession number: MM123456 , M12345 , MM_123456
         2. if there's only one '#' in the sequence and it appears at the end, then no need to remove this sequence
'''

# Inputs ================================================================================================
AADir = r"/Users/Han/Documents/Haim Lab(2018 summer)/3.5.19 HCV&kr(rm 61 access nums)/HCV/HCV E1 and E2 USA 1a AA frame 1.fas"
#AADir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.23.19(12-15flu)/B-14-15 AA Sequence(with X).fas"
outputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/3.5.19 HCV&kr(rm 61 access nums)/HCV/"
outputName = "AccessionNumbers(with# & $).txt"
remove1 = '#'
remove2 = '$'
# =======================================================================================================


ACCESSION_MATCHER = compile(r'[A-Za-z]{2}\d{6}$|[A-Za-z]\d{5}$|[A-Za-z]{2}\_\d{6}$')

AAContent = [] # a list for all AA sequence


def readFasta(x, y):  # read the AA Sequence fasta file and then store them in list AAContent
    file = open(x,"r")
    for line in file:
        y.append(line)


readFasta(AADir, AAContent)  # execute the function


AccessionList = []  # a list for all Accession Numbers that contains '#' or '$'
HeaderList = []  # a list contains index of all headers starting with ">"

def getHeaderIndex () :
    
    i = 0
    while i < len(AAContent):
        if AAContent[i][0] == '>':
            HeaderList.append(i)
        i += 1


getHeaderIndex()
print("How many accession numbers in this file: "+ str(len(HeaderList)))


def getAccessNum(string):
    """
    extract accession from the given string, returns the first match if there are multiple matches
    :param string: the string to extract accession from
    :return: the extracted accession
    """
    #print(string)
    return ACCESSION_MATCHER.findall(string)[0]


def findX():  # find 'X' or '?' in the AA sequence and then store the accession number in a list
    count = 0
    i = 0
    while i < (len(HeaderList)-1):
        
        j = 0
        fragment = AAContent[(HeaderList[i]+1):HeaderList[i+1]]
        #print(fragment[-1])
        while j < (len(fragment)-1):

            if (remove1 in (fragment[j])) or (remove2 in (fragment[j])): # check '#' and '$
                if getAccessNum(AAContent[HeaderList[i]]) not in AccessionList:
                    AccessionList.append(getAccessNum(AAContent[HeaderList[i]]))
            j+=1
        # now check if the last line of AA sequence contains only one '#' at the end
        if (remove1 in (fragment[-1][:-2])) or (remove2 in (fragment[-1][:-2])):
           # print(fragment[-1][:-2])
            if (getAccessNum(AAContent[HeaderList[i]]) not in AccessionList):     
                   AccessionList.append(getAccessNum(AAContent[HeaderList[i]]))
        i += 1
    #while loop doesn't check the last sample because of i < (len(HeaderList)-1)
    #now check the last sample to see if it contains #$
    k = 0
    fragment2 = AAContent[(HeaderList[-1])+1:]
    while k < (len(fragment2)-1):
        if (remove1 in fragment2[k]) or (remove2 in fragment2[k]):
           count += 1
           if (getAccessNum(AAContent[HeaderList[-1]]) not in AccessionList):
               AccessionList.append(getAccessNum(AAContent[HeaderList[-1]]))
        k += 1
    
    #print(fragment2[-1][:-2])
    if (remove1 in (fragment2[-1][:-2])) or (remove2 in (fragment2[-1][:-2])):
        
        if (getAccessNum(AAContent[HeaderList[-1]]) not in AccessionList):
               AccessionList.append(getAccessNum(AAContent[HeaderList[-1]]))

        

findX() # execute the function 

def checkDup(): # check the duplicate again in the AccessionList
    i = 0
    while (i<len(AccessionList)):
        for j in AccessionList[i+1:]:
            if AccessionList[i] == j:
                print("find duplicate")  # if there is a duplicate, print it 
                print(j)
        i = i+1
checkDup()

print("How many accession numbers contain either "+remove1+" or "+remove2 +" : " + str(len(AccessionList))) # print the length of AccessionList to double check the number
print('\n')
print("Accession numbers that need to be removed: ")
print("......check out the output txt file......")
#print(AccessionList) # print all the accession numbers that contains '#' or '$'

def writeTxt(x): # write the x into a new text file 
    output= open(outputDir+outputName,"w+") 
    for i in x:
        output.write(i+"\n") # one number one line 
    output.close
writeTxt(AccessionList) # execute the function 
