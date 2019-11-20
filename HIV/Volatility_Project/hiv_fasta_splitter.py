#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 14:06:43 2019

@author: Han
"""

'''
    For HIV Volatility Project:
        Input: raw sequence in fasta format
        The program divides the input fasta file into multiple fasta files based on :
            1. distinct patient name
            2. (optional)distinct year : when patient names are the same, then separate by year
        Output: multiple fasta files and one txt file contains a list of all patient names
        
        format of each sample: 
            >B.FR.1983.LAI.K03455
            MRVKE---KYQHLWRWGWRW-----GTML---LGMLMI-CSA-TEKLWVT............
'''

import itertools

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/11.5.19_hiv_volatility/old_fasta_separate/"
#input_file_name = r"small_test_sample.fas"
input_file_name = r"B_longs_completes.fas"
output_folder_name = r"separated/"  # back slash at the end

separator = '.'   # symbol that separates different attributes
based_on_year = True  # if False, then this program will ignore year and divide sequences only based on patient name
patient_name_pos = (3,4)  # (3,4) means the position of patient name attribute is between the 3rd separator and 4th separator
year_pos = (2,3)  # the position of year attribute
# ==========================================================================================
 
input_file = working_dir + input_file_name
output_folder = working_dir + output_folder_name

input_list = []  # store input file to list
name_seq_dict = {}  # key:name-year, value: [sample1,sample2...]


def read_fasta(x,y): # read a fasta file x and store into a list y
    file = open(x,"r")
    for line in file:
        y.append(line)


def write_fas(x,y): # write the list x into y file
    output= open(y,"w+") 
    for i in x:
        output.write(i)
    output.close


def write_name_list(x,y): # write the name list into y file
    output= open(y,"w+") 
    for i in x:
        if i != x[-1]:
            output.write(f"{i},")
        else:
            output.write(f"{i}")  # no need for ',' for the last name
    output.close


index_list_of_header = []
# x is the input list, return the total sample numbers, use this number to check output
# also generate a list of each header's index
def count_input_total(x): 
    global index_list_of_header
    t_c = 0  # total count
    for i in x:
        if i[0] == '>':
            index_list_of_header.append(x.index(i))
            t_c += 1
    return t_c


# x is the input list, split based on patient name OR name-year
def split_name_year(x): 
    global name_seq_dict
    
    header_i = 0  # use header_i to iterate through index_list_of_header
    while header_i < len(index_list_of_header):  # this loop constructs the dictionary name:[sample]
        sepor_index_list = []  # a list of a hear's each separator's index
        name = None  # save this patient's name here later
        year = None  # save this patient's year here later
        #print(x[index_list_of_header[header_i]])
        sep_i = 0  # use sep_i to iterate through each header, and record each separator's index to sepor_index_list
        while sep_i < len(x[index_list_of_header[header_i]]):  # iterate a header
            if (x[index_list_of_header[header_i]][sep_i]) == separator:  # find separator
                sepor_index_list.append(sep_i)
                sep_i += 1
            else:
                sep_i += 1
        #print(sepor_index_list)
        name = (x[index_list_of_header[header_i]])[(sepor_index_list[patient_name_pos[0]-1]+1):(sepor_index_list[patient_name_pos[1]-1])]        
        year = (x[index_list_of_header[header_i]])[(sepor_index_list[year_pos[0]-1]+1):(sepor_index_list[year_pos[1]-1])]
        
        if based_on_year == True:   # divide based on both name and year
            if (f"{name}-{year}") not in name_seq_dict:
                name_seq_dict[f"{name}-{year}"] = []
                if index_list_of_header[header_i] != index_list_of_header[-1]:  # check if it is the end of input fasta
                    name_seq_dict[f"{name}-{year}"].append(x[(index_list_of_header[header_i]):(index_list_of_header[header_i+1])])
                else:
                    name_seq_dict[f"{name}-{year}"].append(x[(index_list_of_header[header_i]):])
            else:
                if index_list_of_header[header_i] != index_list_of_header[-1]:
                    name_seq_dict[f"{name}-{year}"].append(x[(index_list_of_header[header_i]):(index_list_of_header[header_i+1])])
                else:
                    name_seq_dict[f"{name}-{year}"].append(x[(index_list_of_header[header_i]):])
        if based_on_year == False:  # divide only based on name
            if (f"{name}") not in name_seq_dict:
                name_seq_dict[f"{name}"] = []
                if index_list_of_header[header_i] != index_list_of_header[-1]:
                    name_seq_dict[f"{name}"].append(x[(index_list_of_header[header_i]):(index_list_of_header[header_i+1])])
                else:
                    name_seq_dict[f"{name}"].append(x[(index_list_of_header[header_i]):])
            else:
                if index_list_of_header[header_i] != index_list_of_header[-1]:
                    name_seq_dict[f"{name}"].append(x[(index_list_of_header[header_i]):(index_list_of_header[header_i+1])])
                else:
                    name_seq_dict[f"{name}"].append(x[(index_list_of_header[header_i]):])
        
        header_i += 1  # go to next header
    return

    

def main():
    read_fasta(input_file,input_list)  # read input fasta file
    correct_total_count = count_input_total(input_list)  # total count of the input fasta file
    split_name_year(input_list)  # 
    name_list = list(name_seq_dict.keys())  # list contains distinct patient identifier : name OR name-year
    
    for i in name_seq_dict:
        print(f"{i} : {len(name_seq_dict[i])}samples")
    
    print(f"\n* Input fasta contains {correct_total_count} samples.\n")
    print(f"* Found {len(name_list)} distinct patients total.\n")
    file_count = 0  # count the number of files generated
    for i in name_seq_dict:
        if len(name_seq_dict[i])>1:
            flat_list = list(itertools.chain(*(name_seq_dict[i])))
            write_fas(flat_list, f"{output_folder}{i}.fas")
            file_count += 1
        else:
            write_fas(name_seq_dict[i][0], f"{output_folder}{i}.fas")
            file_count += 1
    
    write_name_list(name_list, f"{output_folder}allPatientNames.txt")
    
    print(f"* Number of files generated: {file_count + 1}, including: ")
    print(f"    {file_count} fasta files and 1 allPatientNames.txt")

    check_total_count = 0  # check if the total sample number matches the correct total number
    for i in name_seq_dict:
        check_total_count += len(name_seq_dict[i])
    if check_total_count == correct_total_count:
        print("\n checking total sample count ............. CORRECT! ")
    else:
        print("\n checking total sample count ............. TOTAL NUMBER WRONG!!! ")


main()












