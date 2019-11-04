#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 14:34:27 2019

@author: Changze Han
"""
'''
    For FLU project
    This script goes through each sequence and Search & Count the number of letter 
    that's not A C T G. Then clean the data by removing sequences that 
    contains more than 1 non-ACTG letter. ( '-' and ' ' and '\n'are ignored)
    
    IMPORTANT: currently, this script only works for sequences with only accession number as 
               their properties. When more properties(country, year) are selected, some parts 
               need to be updated. 
    
    INPUT: Nucleotide fasta file
    OUTPUT: 1. sequences that are cleaned (fas file, expected output)
            2. a list a accession numbers that are removed (txt file, can be deleted)
            3. sequences that are removed (fas file, can be deleted)
            
            4. double check file (for debugging, can be deleted)
            5. double check file (for debugging, can be deleted)
'''

from re import compile

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/10.25.19_H3N2/human/15-19_season_USA/"
fas_name = "B.human_15-19_season_H3N2_USA_nucl_aligned_9515.fas"
out_name = "C.human_15-19_season_H3N2_USA_nucl_aligned_9515_cleaned.fasta"  
non_ACTG_count_cutoff = 1  # if seen >1 1 non-ACTG letter then remove this accession
# ==========================================================================================

fas_input = working_dir + fas_name
out_acc_list = working_dir + "rm_acc_list.txt"
out_rm_seq = working_dir + "rm_seq.fas"
out_clean_seq = working_dir + out_name
ACCESSION_MATCHER = compile(r'[A-Za-z]{2}\d{6}|[A-Za-z]{1}\d{5}|[A-Za-z]{3}\d{5}')
nucleotide_seq = ('A','C','T','G','-',' ','\n')

def readFasta(x,y): # read a fasta file x and store into a list y
    file = open(x,"r")
    for line in file:
        y.append(line)
        
        
def write(x,y): # write the list x into y file
    output= open(y,"w+") 
    for i in x:
        output.write(i)
    output.close


def getAccessNum(string):
    #extract accession from the given string, returns the first match if there are multiple matches
    return ACCESSION_MATCHER.findall(string)[0]

fas_input_list = []  # original data
rm_acc_list = []  # accession number list of removed 
rm_acc_seq = []  # accession number + sequence of removed 
clean_seq = []  # rest seq

def search_count():
    length = len(fas_input_list)  
    index = 1  #starting index of sequence : 1 3 5 7 ...
    while (index < length):
        count = 0  # reset to 0, keep track of count of non-ACTG letter
        for i in fas_input_list[index]:
            if (count > non_ACTG_count_cutoff):  # more than 1 non-ACTG letter appeared
                rm_acc_list.append(getAccessNum(fas_input_list[index-1])+"\n")  # add accession num 
                '''this part need to update when more properties are used'''
                rm_acc_seq.append(">"+getAccessNum(fas_input_list[index-1])+"\n") 
                rm_acc_seq.append(fas_input_list[index])
                break
            else:
                if i not in nucleotide_seq:
                    #print(i)
                    count += 1
        #print("=========")
        index = index + 2
            


def remove():  # if access not in rm_acc_list, then append to clean_seq
    length = len(fas_input_list) 
    index = 0  # starting index of properties : 0 2 4 6 ...
    while (index < length):
        if ((getAccessNum(fas_input_list[index])+"\n") not in rm_acc_list):
            #print(getAccessNum(fas_input_list[index]))
            '''this part need to update when more properties are used'''
            clean_seq.append(">"+getAccessNum(fas_input_list[index])+"\n")
            clean_seq.append(fas_input_list[index+1])
        index = index + 2
    

readFasta(fas_input, fas_input_list)  # import fas input to a list
search_count()    # filter out all non-valid accession numbers and sequences
remove()
print(f"how many in original file: {int(len(fas_input_list)/2)}")
print(f"how many removed:  {len(rm_acc_list)}\n removed lists: \n{rm_acc_list}\n")
print(f"double check how many removed: {int(len(rm_acc_seq)/2)}\n")
print(f"how many left: {int(len(clean_seq)/2)}")
write(rm_acc_list, out_acc_list)
write(rm_acc_seq, out_rm_seq)
write(clean_seq, out_clean_seq)

# TEST, double check removed sequences   
i = 1
rm = []
while (i < len(rm_acc_seq)):
    for j in rm_acc_seq[i]:
      
        if j not in nucleotide_seq:
            rm.append(j)
    i = i + 2
    rm.append("======")

write(rm,working_dir+"check_rm.txt" )

# TEST, double check clean sequences  
i = 1
clean = []
while (i < len(clean_seq)):
    for j in clean_seq[i]:
        
        if j not in nucleotide_seq:
            clean.append(j)
    i = i + 2
    clean.append("======")

write(clean,working_dir+"check_clean.txt" )
