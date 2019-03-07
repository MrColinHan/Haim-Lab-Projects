#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 15:05:31 2019

@author: Han
"""

'''
    This script removes Accession groups in a Nucleotide sequence fasta file based 
    on the Accession numbers I found in the AA Sequence. Since 'X' and '?' only appear
    in AA Sequence which is converted from a Nucleotide sequence, i can only find them in 
    AA sequence first then remove the same accession numbers in a nucleotide sequence
    
    INPUTS: 
            lefroverDir: directory of the Accession numbers that contain 'X' or '?'
                         ( output of the "Find'X'inAAsequence.py" )
            NucleotideDir: directory of the nucleotide sequence fasta file
            outputDir: directory of the output file
            outputName: directory of the output file
'''



# Inputs ###############################################################################################
leftoverDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.23.19(12-15flu)/C-14-15 AccessionNumbers(withX).txt"
NucleotideDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.23.19(12-15flu)/A-2014-2015 USA H3N2 nucleotide(1929samples).fasta"
outputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/1.23.19(12-15flu)/"
outputName = "D-14-15 Nucleotide(withoutX).fas"
########################################################################################################



fasContent = [] # a list for all nucleotide sequence 
TXTContent = [] # a list for all accession numbers that contain 'X' or '?'

def readFasta(x,y): # read a fasta file x and store into a list y
    file = open(x,"r")
    for line in file:
        y.append(line)
readFasta(NucleotideDir,fasContent) # read the nucleotide sequence into fasContent list


print("TXT file (accession numbers with ? or X): ")
def readTXT(): # read a text file into a list
    file = open(leftoverDir,'r+')
    rows = file.readlines()
    for i in rows:
        TXTContent.append(i[0:8])
    file.close()
readTXT()
print(TXTContent) # print out the text file
print('There are '+ str(len(TXTContent))+ ' accession numbers need to be removed.')

print("\n")
print("Fasta File: ")
def NumRowsEachAccession(): # check how many rows does a accession number have in the nucleotide
                            # sequence fasta file. The fasta format might be different for different
                            # files, so we need to check the number of rows. With this number, I 
                            # will know how many rows I need to skip when I want to remove a accession number 
    rowCounts = 1
    if fasContent[0][0] == '>':  # make sure the fasta format is correct (starts with a '>')
        for i in fasContent[1:]:
            if i[0] != '>':
                rowCounts = rowCounts+1
            else:
                return (rowCounts)
    else:
        print("this file doesnt start with '>', make sure the input file is in Fasta format")

NumRowsPerAccessionNum = NumRowsEachAccession() # store the number of rows 
print("Each Accession number has "+ str(NumRowsPerAccessionNum)+ " rows(for debugging)")


AccessFasList = [] # a list for all accession numbers of the nucleotide sequence
def AccessInFas(x): # store all accession numbers of fasta file x into a list
                    # (for debugging)
    i = 0
    while i < len(x):
        AccessFasList.append(x[i][1:9])
        i = i + NumRowsPerAccessionNum

AccessInFas(fasContent)
print("before removing, input fasta has " + str(len(AccessFasList))+ " samples.")
'''
AccessCSVList = []
def AccessInCSV():
    for i in csvContent[1:]:
        AccessCSVList.append(i[0])

AccessInCSV()
print("leftover CSV has "+str(len(AccessCSVList)))
'''
def remove(): # Remove the accession numbers contain 'X' or '?'
              # and then write the remaining into a new fasta file 
    i = 0
    output= open(outputDir+outputName,"w+") 
    while i < len(fasContent):
        if fasContent[i][1:9] in TXTContent:
            i = i+NumRowsPerAccessionNum
        else:
            output.write(fasContent[i])
            i = i+1
    output.close
remove()

# check the length of output fasta file contents again 
# if the len(leftover)+len(outputFas) == len(inputFas), then it's correct
outputFasContent = [] # a list for all sequence of output nucleotide fasta file
readFasta(outputDir+outputName,outputFasContent) # read the output fasta file into a list  

AccessFasList = [] # set the list to empty again
AccessInFas(outputFasContent) # read the accession numbers of output fasta into a list 
print("after removing, output fasta has " + str(len(AccessFasList))+ " samples.")
print(str(len(TXTContent))+ "+" +str(len(AccessFasList))+" = "+ str(len(TXTContent)+len(AccessFasList)))








