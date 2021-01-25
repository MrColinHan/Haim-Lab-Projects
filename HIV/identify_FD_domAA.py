#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 11:50:05 2019

@author: Han
"""

'''
    For HIV Project: (single sample ) (also works for long now if each identifier is 'Patient-Day'): 
        This program identifies each patient's dominant AA in each position. 
        In addition, it also identifies whether this AA is volatile (meaning whether fd of this AA is 100%)
        
        Input: A folder contains multiple FD outputs (calculated by flu_fd_stdev_cal.py). 
               Each file is one patient's fd. Each file's name format must be: FD(patient name).csv
               
               A folder contains all buffer files for each patient. 
               Use files in this folder to accurately determine sample count. File name format: Buffer(patient name).csv
        
        Output:  a csv 
                output format: (Z-1 meaning: dominant AA is Z and it's 100%, N-0 meaning: dominant AA is N and it's not 100%)
                    
                    #ofSample | Patient |  1  |  2  |  3  | ...
                        10    |   abc   | Z-1 | N-0 | Z-0 | ...
                        
        
        Note: Sometimes there might be an error caused by .DS_Store file while reading the input folder. 
              Use this cmd in the terminal : " find . -name '.DS_Store' -type f -delete " 
'''

import csv 
import os
# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/1.12.21_flu_tree/fd&std_output/each_group_FD&stdev(afterFuse)/"
fd_val_folder_name = r"fd_values/"  # name of the folder that holds all fd values, slash at the end
fd_buf_folder_name = r"fd_buffers/"
output_name = r"dominant_AA.csv"

position_range = (1, 550)

patient_name_col = 1 #2  # col index of patient name in Buffer files, index starts at 0 (NOT 1)

# ==========================================================================================

fd_val_folder = working_dir + fd_val_folder_name
fd_buf_folder = working_dir + fd_buf_folder_name
output_file = working_dir + output_name

cur_pat_name = None  # store the name of current patient
cur_pat_fd_list = []  # store current patient's csv fd file
cur_pat_buf_list = []  # store current patient's csv buffer file

cur_pat_output_list = []
final_output_list = []  # store final outputs 


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


def extract_pat_name(x) : # extract patient name from string x which is in format of "FD(UNC5539).csv"
    print(x)  # sometimes there could be .DS_Store file causing trouble
    left_parenthesis_index = x.index("(")
    right_parenthesis_index = x.index(")")
    #for i,j in enumerate(x):
    return x[left_parenthesis_index+1 : right_parenthesis_index]  


def get_pos_list(x): # x is a tuple e.g.: (3,8), return a list of position (3,4,5,6,7,8)
    return list(range(x[0], x[1]+1))

def find_dominant(x, y): # x is one fd file in a list, y is the position list
    return_list = []  # return this list as output  [Z-1, Z-0, N-0, H-1, ...]
    aa_index = {'Z':0
                ,'N':0
                ,'T':0
                ,'S':0
                ,'D':0
                ,'E':0
                ,'K':0
                ,'R':0
                ,'H':0
                ,'Y':0
                ,'Q':0
                ,'I':0
                ,'L':0
                ,'V':0
                ,'A':0
                ,'C':0
                ,'F':0
                ,'G':0
                ,'M':0
                ,'P':0
                ,'W':0}
    # construct the aa-index dictionary incase the input file has different AA order
    for row_i in range(len(x)):  # row_i is index of row
        if x[row_i][0] in aa_index: 
            aa_index[x[row_i][0]] = row_i
    
    for i in y: # iterate through the position list
        current_position_index = x[0][1:].index(str(i)) # get the col index of this position
        current_pos_dominant = None
        for aa in aa_index: 
            if float(x[aa_index[aa]][1:][current_position_index]) > 50:  # [aa_index[aa]] locates the row, [current_position_index] locates the col
                if float(x[aa_index[aa]][1:][current_position_index]) == 100: 
                    current_pos_dominant = f"{aa}-1"
                else:
                    current_pos_dominant = f"{aa}-0"
        if current_pos_dominant == None: 
            current_pos_dominant = "None"
        return_list.append(current_pos_dominant)
    return return_list


def main(): 
    global cur_pat_fd_list
    global cur_pat_buf_list 
    global cur_par_name
    global final_output_list
    global cur_pat_output_list
    
    overall_count = 0  # count the total sample number while going through each file 
    position_list = get_pos_list(position_range)  # get the target position list

    final_output_list.append(["#ofSample"] + ["Patient"] + position_list)
    for filename in os.listdir(fd_val_folder):  # iterate through each fd file 
        cur_pat_fd_list = []  # reset
        cur_pat_buf_list  = [] # reset
        cur_pat_name = None # reset
        cur_pat_output_list = [] # reset
        
        cur_pat_name = extract_pat_name(filename)
        try: # read the fd file
            read_csv (fd_val_folder + filename, cur_pat_fd_list)  # read one file to current patient list
        except: 
            raise ValueError (f"FD Input file Error: {cur_pat_name}")
        
        try: # read the corresponding buffer file in another folder
            read_csv(f"{fd_buf_folder}Buffer({cur_pat_name}).csv", cur_pat_buf_list)
        except: 
            raise ValueError (f"Buffer Input file Error: {cur_pat_name}")
            
        
        if cur_pat_name == cur_pat_buf_list[1][patient_name_col]: # double check if the buffer patient name matches the patient name in fd
            print(f"{cur_pat_name} : {len(cur_pat_buf_list)-1} ")  
        else:
            raise ValueError (f"Filename doesn't match patient name in Buffer file : {cur_pat_name}")
            
        overall_count += len(cur_pat_buf_list)-1
        
        cur_pat_output_list = find_dominant(cur_pat_fd_list, position_list)
        cur_pat_output_list.insert(0,cur_pat_name)  # add this patient's name
        cur_pat_output_list.insert(0,len(cur_pat_buf_list)-1)  # add sample count
        
        final_output_list.append(cur_pat_output_list)
        
    write_csv(final_output_list, output_file)  # write the final csv output
    print(f"\nOverall sample count: {overall_count}")
        
main()




























