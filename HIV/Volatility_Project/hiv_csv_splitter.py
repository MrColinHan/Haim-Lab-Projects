#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 15:42:05 2019

@author: Changze Han
"""

'''
    For HIV Volatility Project:
        Input: sequences in CSV format
        The program divides the input csv file into multiple fasta files based on :
            1. distinct patient name
            2. distinct year : when patient names are the same, then separate by year
            3. distinct days : when patient names and years are same, then separate by days
        Output: multiple fasta files and one txt file contains a list of all patient names
                 file name format :   name.fas
                                      name-year.fas
                                      name-days.fas  (theoretically, result of 'name-days' equivalent to 'name-years-days')
        
        format of csv file: 
            | Country | Year | Patient | Days | Accession | 1 | 2 | 3 | ...
            |    FR   | 1983 |   LAI   |  30  |   K03455  | M | R | V | ...
            ...
            ...
'''


import csv

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/12.5.19_hiv_single/fd/B_NA/"
#input_file_name = r"small_test_sample.csv"
input_file_name = r"B_NA_single_PNGS_2660.csv"
output_format = 'csv'  # select output formats : 'csv'  or 'fasta'
output_folder_name = r"test_separated(check fd_buffer)/"  # slash at the end

# Column number of each attribute  !!! Col count start from 0, NOT 1 !!!
patient_name_col = 2 
year_col = 1  
days_col = 3  
seq_start_col = 4#5 # start column number of sequences which is position 1

identifier_format = 'name'   # choose from three formats below
# avaliable formats:  'name'    'name-year'    'name-days' 
sample_num_cutoff = 0  # groups contain <= cutoff samples will be dropped

# =========================================================================================
csv_input_file = working_dir + input_file_name
output_folder = working_dir + output_folder_name

csv_input_list = []  # store input file to list
name_seq_dict = {}  # key:name-year-days, value: [sample1,sample2...]
                    # {a-2005-100:[row1,row2,row3...], b-1995-0:[row1,row2,row3...], ...}
check_total_count = 0  # check the total sample number count during the writing process
check_fas_file_count = 0  # check the total count of fasta files wrote
name_list_after_cut = []  # name list after cutoff


def read_csv(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row) 
        

def write_fas(x,y): # write the list x into y file
    output= open(y,"w+") 
    for i in x:
        output.write(i)
    output.close


def write_csv(x,y):  # write list x into file y
    with open(y,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()
    

def write_name_list(x,y): # write the name list into y file
    output= open(y,"w+") 
    for i in x:
        if i != x[-1]:
            output.write(f"{i},")
        else:
            output.write(f"{i}")  # no need for ',' for the last name
    output.close


# x is the input list, take x and sep into the dictionary
def sep(x):  
    global name_seq_dict
    
    for i in x[1:]: # ignore the first header row
        
        # select the identifier format
        if identifier_format == 'name':   
            key = f"{i[patient_name_col]}" 
        elif identifier_format == 'name-year': 
            key = f"{i[patient_name_col]}-{i[year_col]}" 
        elif identifier_format == 'name-days': 
            key = f"{i[patient_name_col]}-{i[days_col]}" 
        else:
            raise ValueError("Identifier Format WRONG !!!")
        # construct dictionary
        if key not in name_seq_dict: # not found key in dict
            name_seq_dict[key] = []  # add key
            name_seq_dict[key].append(i)  # add this csv row to dict value list
        else:   # found key in dict  
            name_seq_dict[key].append(i)  # add this csv row to dict value list


def write_dict_to_fas_or_csv(d,h): # write the dict into multiple fasta files; h is the header row for csv output
    global check_total_count  # save total sample numbers during writing
    global check_fas_file_count  # save total count of fasta files generated
    global name_list_after_cut
    for i in d:  # go through name lists
        fas_list = []  # save this key's sequences to this list in order to write a fasta file
        if len(d[i]) > sample_num_cutoff:  # apply sample number cutoff
            for j in d[i]:  # j was a row as a list in the csv, will be divided into 2 rows in fas
                fas_list.append('>'+'.'.join(j[:seq_start_col]) + '\n')  # 1st row in fas, new line at the end
                fas_list.append(''.join(j[seq_start_col:]) + '\n')  # 2nd row in fas, new line at the end
                check_total_count += 1  # add one to the final count
            if output_format == 'fasta':
                write_fas(fas_list, f"{output_folder}{i}.fas")  # write a fas file
            elif output_format == 'csv': 
                temp_csv_list = [] # save this key's sequences to this list in order to write a csv file
                temp_csv_list = d[i].copy()
                print(len(temp_csv_list))
                temp_csv_list.insert(0,h)
                write_csv(temp_csv_list, f"{output_folder}{i}.csv")
            name_list_after_cut.append(i)  # construct after_cutoff group name list
            check_fas_file_count += 1  # file count + 1


def main():
    read_csv(csv_input_file, csv_input_list)
    sep(csv_input_list)  # construct the dictionary
    original_name_list = list(name_seq_dict.keys())  # list contains all distinct patient identifier (before cutoff)
    write_dict_to_fas_or_csv(name_seq_dict, csv_input_list[0])  # write fasta files (also apply the sample number cutoff)
    write_name_list(name_list_after_cut, f"{output_folder}allPatientNames.txt")
    
    for i in name_list_after_cut:  # print each group's sample number
        print(f"{i} : {len(name_seq_dict[i])} samples")
        
    print(f"\n* Input csv contains {len(csv_input_list)-1} samples.")
    print(f"* Found {len(original_name_list)} distinct {identifier_format} groups.\n")
    
    print(f"* After cutoff: {check_total_count} samples left.")
    print(f"* After cutoff: {len(name_list_after_cut)} distinct {identifier_format} groups left. \n")
    
    print(f"* Number of files generated: {check_fas_file_count+1}, including: ")
    if output_format == 'fasta':
        print(f"    {check_fas_file_count} fasta files and 1 allPatientNames.txt")
    elif output_format == 'csv':
        print(f"    {check_fas_file_count} csv files and 1 allPatientNames.txt")


main()  # run the entire program




























