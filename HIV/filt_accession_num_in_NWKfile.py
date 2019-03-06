#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 16:47:00 2019

@author: Han
"""

'''
    This script takes a tree format .NWK file and filt out all accession numbers from B.KR. 
    An txt format output file will be generated which contains those B.KR accession numbers
    
'''


f=open("/Users/Han/Documents/Haim Lab(2018 summer)/3.4.19 nwk remove kr/Clade B gp120 tree.txt", "r")
outputName = "removed_KR.txt"
out= open("/Users/Han/Documents/Haim Lab(2018 summer)/3.4.19 nwk remove kr/"+outputName, "w+")
contents =f.readlines()
contList =  list(contents[0])

output = []

KR_index = [] # index of char 'R' of B.KR
i = 0
count = 0
while (i < len(contList)):
    if (contList[i] == "B") and (contList[i+1] == ".") and (contList[i+2] == "K") and (contList[i+3] == "R"):
            count += 1
            KR_index.append(i+3)
            
            dotCount = 0
            #DotFound = None
            j = 0
            #print(i+3)
            
            while j < len(contList[i+3:]):

                if contList[i+3:][j] == ".":
                    dotCount += 1
                if dotCount == 3:
                    output.append(contList[i+3:][j+1:j+9])

                    break
                j = j + 1
    i = i + 1
k = 0
while k<len(output):
    emptyList = []
    emptyList.append((''.join(output[k])))
    output[k] = emptyList
    k += 1
    

for i in output:
    out.write(i[0])
    out.write('\n')
out.close()

