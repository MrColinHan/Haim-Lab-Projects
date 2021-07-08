#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 20:14:48 2019

@author: Changze Han
"""

'''
    For Flu:
        
    Convert a cleaned fasta sequence(nucleotide or AA) file to a csv format file. 
    The purpose of this script is innovating a new way for fas->csv conversion. 
    Before today, we've been doing fasta -> tab(use a web tool) -> copy to excel -> apply func in excel. 
    The old procedure was really time consuming. 
    Now: fas --directly--> csv

'''


import csv 
from re import compile

# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/6.14.21/"
fas_input_name = "aligned.fas"
csv_output_name = "aligned.csv"
# ========================================================================================================
fas_input_file = working_dir + fas_input_name
csv_output_file = working_dir + csv_output_name
ACCESSION_MATCHER = compile(r'[A-Za-z]{2}\d{6}|[A-Za-z]{1}\d{5}|[A-Za-z]{3}\d{5}')
fas_input_list = []  # store input fasta contents 
csv_output_list = []  #store outputs, a list of lists/rows

def read_fasta(x,y): # read a fasta file x and store into a list y
    file = open(x,"r")
    for line in file:
        y.append(line)
        

def write_csv(x,y):  # write list x into file y
    with open(y,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()
    

def getAccessNum(string):
    #extract accession from the given string, returns the first match if there are multiple matches
    return ACCESSION_MATCHER.findall(string)[0]


# x is the fas_input_list, construct a list of lists/rows
def construct_output_list(x):  
    fas_i = 0  # iterate fas list
    while fas_i < len(fas_input_list):
        row = []  # a list to store this one row's data in csv
        #row.append(getAccessNum(fas_input_list[fas_i]))  # add accession number
        row.append(fas_input_list[fas_i][1:])  # add ALL Attributes
        row.append(fas_input_list[fas_i+1])  # add seq
        # now add each seq
        for j in fas_input_list[fas_i+1]:
            row.append(j)
        csv_output_list.append(row)
        fas_i += 2


read_fasta(fas_input_file,fas_input_list)
construct_output_list(fas_input_list)
write_csv(csv_output_list,csv_output_file)

print("check: ")
print(f"fasta file contains {int(len(fas_input_list)/2)} samples")
print(f"output csv file contains {len(csv_output_list)} samples")
print(f"\nFirst and last seq in fasta: ")
print(f"{fas_input_list[0]}{fas_input_list[1][:10]}......{fas_input_list[1][-10:-1]}")
print(f"{fas_input_list[-2]}{fas_input_list[-1][:10]}......{fas_input_list[-1][-10:-1]}")
print(f"\nFirst and last seq in CSV output: ")
print(f">{csv_output_list[0][0]}\n{csv_output_list[0][2:12]}......{csv_output_list[0][-10:]}")
print(f">{csv_output_list[-1][0]}\n{csv_output_list[-1][2:12]}......{csv_output_list[-1][-10:]}")










