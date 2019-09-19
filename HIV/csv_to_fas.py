#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 11:16:05 2019

@author: Han
"""

import csv


csv_dir = "/Users/Han/Documents/Haim_Lab(2018_summer)/9.9.19_HIV_newfig/A1_13pos/A1_10-15_13pos.csv"
output_dir = "/Users/Han/Documents/Haim_Lab(2018_summer)/9.9.19_HIV_newfig/A1_13pos/"
output_name = "A1_10-15_13pos.fas"
fas_dir = "/Users/Han/Documents/Haim_Lab(2018_summer)/9.9.19_HIV_newfig/A1_13pos/"+output_name


def readFasta(x,y): # read a fasta file x and store into a list y
    file = open(x,"r")
    for line in file:
        y.append(line)


def readCSV(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row)     


def writeTxt(x): # write the list x into a text file 
    output= open(output_dir+output_name,"w+") 
    for i in x:
        output.write(i+"\n") # one number one line 
    output.close
    
 
csvList = []
output_list = []


readCSV(csv_dir,csvList)  # load csv file into a list

for i in csvList:
    output_list.append(f">{i[0]}")
    output_list.append(f"{i[1]}")


writeTxt(output_list) 

fasContent = [] 
readFasta(fas_dir,fasContent)  # check fas content
print(f"csv content:\n {csvList[:5]}\n")
print(f"fas content:\n {fasContent[:10]}")














