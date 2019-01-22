#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 15:12:13 2019

@author: Han
"""


# this code find Accession numbers which contain 'X' or '?'
# and then put those numbers in a new text file
import csv

AADir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.16.19/AA2640.fas"

outputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.16.19/"
outputName = "2640AccessionWithXandQuestionMark.txt"



AAContent = []

def readFasta(x,y):
    file = open(x,"r")
    for line in file:
        y.append(line)

readFasta(AADir,AAContent)

AccessionList = [] ################
def findX():
    count = 0
    i = 0
    while (i < len(AAContent)):
        if ('?' in AAContent[i]) or ('X' in AAContent[i]):
            count += 1
            if (AAContent[i-1][1:9] not in AccessionList):
                AccessionList.append(AAContent[i-1][1:9])
        i += 1
    print(count)
    
findX()
print(AccessionList)
print(len(AccessionList))


def writeTxt():

    output= open(outputDir+outputName,"w+") 
    for i in AccessionList:
        output.write(i+"\n")

    output.close

writeTxt()

def checkDup():
    i = 0
    while (i<len(AccessionList)):
        for j in AccessionList[i+1:]:
            if AccessionList[i] == j:
                print("find duplicate")
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





