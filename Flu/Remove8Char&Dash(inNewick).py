#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 12:32:48 2019

@author: Han
"""

'''NEED TO be UPDATED: make it work in all situations like a line with multiple dash'''
'''
    This script removed all "8 characters + '-' " in a newick file
    INPUT: 
            f = open("......", "r") : directory of the newick file
            outputName: name of the output file
            out = open("......"+outputName,"w+"): directory of the output file
'''




f=open("/Users/Han/Documents/Haim Lab(2018 summer)/1.22.19/I-15-16 Newick(with dash).txt", "r")
outputName = "J-15-16 Newick(without dash).txt"
out= open("/Users/Han/Documents/Haim Lab(2018 summer)/1.22.19/"+outputName,"w+")
contents =f.readlines()

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
