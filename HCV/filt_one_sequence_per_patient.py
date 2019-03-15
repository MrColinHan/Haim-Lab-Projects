#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 17:55:20 2019

@author: Han
"""
'''
    This script takes a fasta format AA sequence as input and generates a new 
    fasta file collects all first sequence of each patient code 
    
    properties order:
            >1a.US.1978.FM.FM_78.AB079078
            
            >Genetype. Country. Year. Patient Code. Sequence name. Accession number  
    
    1. only take US's patinent
    2. take first sequence of each patient code
    3. if patient code is '_' then ignore
'''

# Inputs ================================================================================================
AADir = r"/Users/Han/Documents/Haim Lab(2018 summer)/3.8 test HCV & distri/hcv/C-HCVNucleotide(without#$)Spain.fas"
outputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/3.8 test HCV & distri/hcv/"
outputName = "(Spain)One_sequence_per_patient.fas"
country = 'ES'  # search from this country 
# =======================================================================================================

output = []
AAContent = [] # a list for all AA sequence


def readFasta(x, y):  # read the AA Sequence fasta file and then store them in list AAContent
    file = open(x,"r")
    for line in file:
        y.append(line)


readFasta(AADir, AAContent)  # execute the function


HeaderList = []  # a list contains index of all headers starting with ">"

def getHeaderIndex (x) : # save all indexes of '>' in list x
    
    i = 0
    while i < len(AAContent):
        if AAContent[i][0] == '>':
            x.append(i)
        i += 1


getHeaderIndex(HeaderList)
print("How many accession numbers in this file: "+ str(len(HeaderList)))

US_locations = [] # collect patients from this list 
def find_country(x,y):  # find country 'x' of each patient, if find it then save its idex in y
    for i in HeaderList: 
        dot_one_index = 0
        dot_two_index = 0
        j = 0
        while j < len(AAContent[i]):
            if (dot_one_index == 0) & (AAContent[i][j] == '.'):
                dot_one_index = j
                
            elif (dot_two_index == 0) & (AAContent[i][j] == '.'):
                dot_two_index = j
                if (AAContent[i][(dot_one_index+1):dot_two_index]) == x:
                    y.append(i)
            j += 1
            
find_country(country, US_locations)

#for i in US_locations:
    #print(AAContent[i])

# now take first shown patient code into a list
fist_patientcode_index = [] # not index in AAContent, it's index in US_locations
fist_patientcode_name = []
def find_first_patient(x,y): # in x, find all first shown patient code, save index in y
    i = 0
    while i < len(x):
        dot_count = 0 # take the string between dot 3 and dot 4
        dot_third_index = 0
        dot_forth_index = 0
        j = 0
        while j < len(AAContent[x[i]]):
            if AAContent[x[i]][j] == '.':
                dot_count += 1
            if (dot_count == 3) & (dot_third_index == 0):
                dot_third_index = j
                
            if (dot_count == 4) & (dot_forth_index == 0):
                dot_forth_index = j
                if (AAContent[x[i]][(dot_third_index+1):dot_forth_index]) != '_' and (
                        AAContent[x[i]][(dot_third_index+1):dot_forth_index]) not in fist_patientcode_name:
                    fist_patientcode_name.append((AAContent[x[i]][(dot_third_index+1):dot_forth_index]))
                    y.append(x[i])
                    
                
            j += 1
        i += 1
    

find_first_patient(US_locations,fist_patientcode_index)
print('\n')
print('There are '+str(len(fist_patientcode_index)) + " unique patient code from "+ country +" in this file: ")
print('\n')
print(fist_patientcode_name)
#print(fist_patientcode_index)
print('\n')


#for i in fist_patientcode_index:
    #print(AAContent[i])

match_header = []
def matchindex_in_header(x,y): # x : headerlist, y: fist_patientcode_index
                               # y[0] is the x[match_header[0]]
    
    for i in y: 
        #print(i)
        j = 0
        while j < len(x):
            if i == x[j]:
                match_header.append(j)
                #print(x[j])
            j += 1
    

matchindex_in_header(HeaderList,fist_patientcode_index) 
#print('output:')
def generate_output(x):
    for i in match_header:
        output.append((AAContent[HeaderList[i]:HeaderList[i+1]]))
        
generate_output(output)
#print(output)

def writeTxt(x): # write the x into a new text file 
    output= open(outputDir+outputName,"w+") 
    for i in x:
        for j in i:
            output.write(j) # one number one line 
    output.close
writeTxt(output) # execute the function 
