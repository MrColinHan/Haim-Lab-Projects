#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 12:32:48 2019

@author: Han
"""

# This script remove 

f=open("/Users/Han/Documents/Haim Lab(2018 summer)/1.11/USA 16-17 newick.txt", "r")
outputName = "output.txt"
out= open("/Users/Han/Documents/Haim Lab(2018 summer)/1.11/"+outputName,"w+")
contents =f.readlines()
#contents = f.read()

output = []

for j in contents:
    poslist = []
    pos = -1
    for i in j:
        pos = pos +1
        if i == "-":
            poslist.append(pos)
            #print(poslist)
    
    if len(poslist) == 0:
        output.append(j)
    
    if len(poslist) == 1:
        for i in poslist:
            output.append(j[:i-8]+j[i+1:])
    if len(poslist) > 1:
        output.append(j)
        print("multiple dash at " + str(contents.index(j))+"th line")
        
        
for i in output:
    out.write(i)
out.close()
