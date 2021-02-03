#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 10:46:11 2019

@author: Changze Han
"""

'''
    For Flu project
    Match cleaned_pngs_AA_sequence_CSV file with all_attributes_CSV file
    IMPORTANT: 
        In sequence file: 1. Only two attributes are allowed (Accession, Sequence)
                          2. 'Accession' must be the first attribute and 'Sequence' is the second.  
'''


import csv 


# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/1.20.21_H3N2_H1N1/H1N1/"
seq_filename = r"J.09-20_season_H1N1_USA_AA_5980.csv"
attributes_filename = r"D.attributes_07-20.csv"
output_filename = r"K.09-20_season_H1N1_USA_AA_5980_w_Attributes.csv"

accession_attribute_name = 'Sequence Accession' #'GenBank Protein Accession # this is the name of accession attribute appears in the all_attributes_file
# ==========================================================================================

seq_file = working_dir + seq_filename
atb_file = working_dir + attributes_filename
out_file = working_dir + output_filename

seq_list = []  # list store seq file
atb_list = []  # list store attribute file
acc_col_index = None  # index of accession_attribute_name in the all_attributes_file
attr_dict = {}  # store the acc-attr_dict
out_list = []  # store output lists


def read_csv(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row) 
    
        
def write_csv(x,y):  # write list x into file y
    with open(y,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


# find the index of accession_attribute_name in the all_attributes_file, because the order
# of all attributes are unpredictable 
def find_acc_index():  
    global acc_col_index
    acc_col_index = atb_list[0].index(accession_attribute_name)


def acc_attr_dict():  # construct a dict {'acc1':[all attributes], 'acc2':[all attributes], ...}
    for i in atb_list[1:]:  # exclude header row
        attr_dict[i[acc_col_index]] = i
        

def match():
    global out_list
    out_list.append(atb_list[0] + seq_list[0][1:])  #add header row to output list
    for i in seq_list[1:]:  # exclude header row
        temp_list = attr_dict[i[0].strip()] + i[1:]
        out_list.append(temp_list)


read_csv(seq_file, seq_list)  # load the sequence file
read_csv(atb_file, atb_list)  # load the all_attributes file
find_acc_index()  # find the index of accession_attribute_name
acc_attr_dict()  # construct the dict
match()  # match seq and all_attributes
write_csv(out_list, out_file)  # write out file

# check
print(f"Input sequence file contains {len(seq_list)-1} samples")
print(f"Input attributes file contains {len(atb_list)-1} samples \n")
if (len(seq_list)-1) != (len(out_list) - 1):
    print("!!!OUTPUT SAMPLE NUMBER DOESN'T MATCH!!! SOMETHING WRONG!!!")
    print(f"Output sequence file contains {len(out_list) - 1} samples")
else:
    print(f"Correct ! Output sequence file contains {len(out_list) - 1} samples")









