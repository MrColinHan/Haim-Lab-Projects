#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 15:12:13 2019

@author: Han
"""


# this code find Accession numbers which contain 'X' or '?'
# and then put those numbers in a new text file
import csv

AADir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.16.19/16-17 USA AA sequence.fas"
#AADir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.16.19/AATest.fas"
outputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.16.19/"
outputName = "output.txt"



AAContent = []

def readFasta(x,y):
    file = open(x,"r")
    for line in file:
        y.append(line)

readFasta(AADir,AAContent)

AccessionList = [] ################
def findX():
    count = 0
    for i in AAContent: 
        if ('?' in i) or ('X' in i):
            
            if (AAContent[AAContent.index(i)-1][1:9] not in AccessionList):
                count = count + 1 
                AccessionList.append(AAContent[AAContent.index(i)-1][1:9])
            
            
    print (count)
    
findX()
print(AccessionList)
print(len(AccessionList))

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






def checkDup():
    i = 0
    while (i<len(AccessionList)):
        for j in AccessionList[i+1:]:
            if AccessionList[i] == j:
                print("find duplicate")
                print(j)
        i = i+1
checkDup()
            


def writeTxt():

    output= open(outputDir+outputName,"w+") 
    output.write(AAContent[0])
    output.write(AAContent[1])
    output.write(AAContent[2])

    output.close

writeTxt()